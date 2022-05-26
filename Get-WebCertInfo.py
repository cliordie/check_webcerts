from OpenSSL import SSL
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna
from sites import sitelist
import socket


from collections import namedtuple

HostInfo = namedtuple(field_names='cert hostname peername', typename='HostInfo')

def verify_cert(cert, hostname):
    # verify notAfter/notBefore, CA trusted, servername/sni/hostname
    cert.has_expired()
    # service_identity.pyopenssl.verify_hostname(client_ssl, hostname)
    # issuer

def get_certificate(hostname, port):
    err = 0
    hostname_idna = idna.encode(hostname)
    sock = socket.socket()
    sock.settimeout(3)
    try:
        sock.connect((hostname, port))
    except socket.error:
        print ("Web Service does not appear to be running on",hostname)
        err = 1

    if err == 0:
        peername = sock.getpeername()
        ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
        ctx.check_hostname = False
        ctx.verify_mode = SSL.VERIFY_NONE

        sock_ssl = SSL.Connection(ctx, sock)
        sock_ssl.set_connect_state()
        sock_ssl.set_tlsext_host_name(hostname_idna)
        sock_ssl.do_handshake()
        cert = sock_ssl.get_peer_certificate()
        crypto_cert = cert.to_cryptography()
        sock_ssl.close()
        sock.close()
        return HostInfo(cert=crypto_cert, peername=peername, hostname=hostname)

def get_alt_names(cert):
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return None

def get_common_name(cert):
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def get_issuer(cert):
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None


def print_basic_info(hostinfo):
    hostname=hostinfo.hostname,
    commonname=get_common_name(hostinfo.cert),
    SAN=get_alt_names(hostinfo.cert),
    issuer=get_issuer(hostinfo.cert),
    issuer_txt=issuer[0]
    notafter=hostinfo.cert.not_valid_after

    print("Issuer:          ",issuer_txt)
    print("Expiration Date: ",notafter)


def get_cert_info(hostname):
    hostinfo = get_certificate(hostname, 443)
    print_basic_info(hostinfo)
    

for ip in sitelist:
    siteaddr=socket.gethostbyaddr(ip)
    hostname=siteaddr[0]
    print("IP Address:      ",ip)
    print("Hostname:        ",hostname)
    get_cert_info(hostname)

