import asyncio
import click
import datetime
import itertools
import select
import socket
import ssl
import sys
import OpenSSL


class Domain(str):
    def __new__(cls, domain):
        if domain.startswith('!'):
            name = domain[1:]
        else:
            name = domain
        host = name
        port = 443
        if ':' in name:
            host, port = name.split(':')
            port = int(port)
        connection_host = host
        if '|' in name:
            host, connection_host = name.split('|')
            name = host
        result = str.__new__(cls, name)
        if domain.startswith('!'):
            result.no_fetch = True
        else:
            result.no_fetch = False
        result.host = host
        result.connection_host = connection_host
        result.port = port
        return result


def get_cert_from_domain(domain):
    if domain.no_fetch:
        return (domain, None)
    try:
        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
        sock = OpenSSL.SSL.Connection(ctx, socket.socket())
        sock.settimeout(5)
        sock.set_tlsext_host_name(domain.encode('ascii'))
        sock.connect((domain.connection_host, domain.port))
        while True:
            try:
                sock.do_handshake()
                break
            except OpenSSL.SSL.WantReadError:
                select.select([sock], [], [])
        data = sock.get_peer_cert_chain()
    except socket.gaierror:
        raise
    except Exception as e:
        data = repr(e)
    return (domain, data)


def close_event_loop(loop):
    # just a separate function, so this can be monkeypatched in tests
    loop.close()


def get_domain_certs(domains):
    loop = asyncio.get_event_loop()
    (done, pending) = loop.run_until_complete(asyncio.wait([
        loop.run_in_executor(None, get_cert_from_domain, x)
        for x in itertools.chain(*domains)]))
    close_event_loop(loop)
    return dict(x.result() for x in done)


def domain_key(d):
    return tuple(reversed(d.split('.')))


def check(domainnames_certs, expiry_warn=14):
    msgs = []
    domainnames = set(dnc[0].host for dnc in domainnames_certs)
    earliest_expiration = None
    today = datetime.datetime.utcnow()
    for domain, cert_chain in domainnames_certs:
        if cert_chain is None:
            continue
        if not any(isinstance(cert, OpenSSL.crypto.X509) for cert in cert_chain):
            msgs.append(
                ('error', "Couldn't fetch certificate for %s.\n%s" % (domain, cert_chain)))
            continue
        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
        ctx.set_default_verify_paths()
        store = ctx.get_cert_store()
        for index, cert in reversed(list(enumerate(cert_chain))):
            sc = OpenSSL.crypto.X509StoreContext(store, cert)
            try:
                sc.verify_certificate()
            except OpenSSL.crypto.X509StoreContextError as e:
                msgs.append(
                    ('error', "Validation error '%s'." % e))
            if index > 0:
                store.add_cert(cert)
        cert = cert_chain[0]
        expires = datetime.datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        if expires:
            if earliest_expiration is None or expires < earliest_expiration:
                earliest_expiration = expires
        issued_level = "info"
        issuer = cert.get_issuer().commonName
        if issuer.lower() == "happy hacker fake ca":
            issued_level = "error"
        msgs.append(
            (issued_level, "Issued by: %s" % issuer))
        if len(cert_chain) > 1:
            sign_cert = cert_chain[1]
            subject = sign_cert.get_subject().commonName
            if issuer != subject:
                msgs.append(
                    ('error', "The certificate sign chain subject '%s' doesn't match the issuer '%s'." % (subject, issuer)))
        sig_alg = cert.get_signature_algorithm()
        if sig_alg.startswith(b'sha1'):
            msgs.append(
                ('error', "Unsecure signature algorithm %s" % sig_alg))
        if expires < today:
            msgs.append(
                ('error', "The certificate has expired on %s." % expires))
        elif expires < (today + datetime.timedelta(days=expiry_warn)):
            msgs.append(
                ('warning', "The certificate expires on %s (%s)." % (
                    expires, expires - today)))
        else:
            # rounded delta
            delta = ((expires - today) // 60 // 10 ** 6) * 60 * 10 ** 6
            msgs.append(
                ('info', "Valid until %s (%s)." % (expires, delta)))
        alt_names = set()
        for index in range(cert.get_extension_count()):
            ext = cert.get_extension(index)
            if ext.get_short_name() != b'subjectAltName':
                continue
            alt_names.update(
                x.strip().replace('DNS:', '')
                for x in str(ext).split(','))
        alt_names.add(cert.get_subject().commonName)
        unmatched = domainnames.difference(alt_names)
        if unmatched:
            msgs.append(
                ('info', "Alternate names in certificate: %s" % ', '.join(
                    sorted(alt_names, key=domain_key))))
            if len(domainnames) == 1:
                name = cert.get_subject().commonName
                if name != domain.host:
                    msgs.append(
                        ('error', "The requested domain %s doesn't match the certificate domain %s." % (domain, name)))
            else:
                msgs.append(
                    ('warning', "Unmatched alternate names %s." % ', '.join(
                        sorted(unmatched, key=domain_key))))
        elif domainnames == alt_names:
            msgs.append(
                ('info', "Alternate names match specified domains."))
        else:
            unmatched = alt_names.difference(domainnames)
            msgs.append(
                ('warning', "More alternate names than specified %s." % ', '.join(
                    sorted(unmatched, key=domain_key))))
    return (msgs, earliest_expiration)


def check_domains(domains, domain_certs):
    result = []
    for domainnames in domains:
        domainnames_certs = [(dn, domain_certs[dn]) for dn in domainnames]
        msgs = []
        seen = set()
        earliest_expiration = None
        (dmsgs, expiration) = check(domainnames_certs)
        for level, msg in dmsgs:
            if expiration:
                if earliest_expiration is None or expiration < earliest_expiration:
                    earliest_expiration = expiration
            if msg not in seen:
                seen.add(msg)
                msgs.append((level, msg))
        result.append((domainnames, msgs, earliest_expiration))
    return result


def domains_from_file(file):
    if not file:
        return
    with open(file, 'r', encoding='utf-8') as f:
        current = []
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.endswith('/'):
                current.append(line)
                continue
            current.append(line)
            yield "".join(current)
            current = []


@click.command()
@click.option('-f', '--file', metavar='FILE', help='File to read domains from. One per line.')
@click.option('-v', '--verbose', count=True, help='Increase verbosity. Can be used several times. Currently max verbosity is 2.')
@click.argument('domain', nargs=-1)
def main(file, domain, verbose):
    """Checks the TLS certificate for each DOMAIN.

       You can add checks for alternative names by separating them with a slash, like example.com/www.example.com.

       Exits with return code 3 when there are warnings and code 4 when there are errors.
    """
    domains = domains_from_file(file)
    domains = itertools.chain(domains, domain)
    domains = [
        [Domain(d) for d in x.split('/')]
        for x in domains
        if x and not x.startswith('#')]
    domain_certs = get_domain_certs(domains)
    total_warnings = 0
    total_errors = 0
    earliest_expiration = None
    for domainnames, msgs, expiration in check_domains(domains, domain_certs):
        if expiration:
            if earliest_expiration is None or expiration < earliest_expiration:
                earliest_expiration = expiration
        warnings = 0
        errors = 0
        domain_msgs = [', '.join(domainnames)]
        for level, msg in msgs:
            if level == 'error':
                color = 'red'
                errors = errors + 1
            elif level == 'warning':
                color = 'yellow'
                warnings = warnings + 1
            else:
                color = None
            if color:
                msg = click.style(msg, fg=color)
            msg = "\n".join("    " + m for m in msg.split('\n'))
            domain_msgs.append(msg)
        if (verbose > 1) or warnings or errors:
            click.echo('\n'.join(domain_msgs))
        total_errors = total_errors + errors
        total_warnings = total_warnings + warnings
    msg = "%s error(s), %s warning(s)" % (total_errors, total_warnings)
    today = datetime.datetime.utcnow()
    if earliest_expiration:
        msg += "\nEarliest expiration on %s (%s)." % (
            earliest_expiration, earliest_expiration - today)
    if total_errors:
        click.echo(click.style(msg, fg="red"))
        sys.exit(4)
    elif total_warnings:
        click.echo(click.style(msg, fg="yellow"))
        sys.exit(3)
    if verbose:
        click.echo(click.style(msg, fg="green"))
