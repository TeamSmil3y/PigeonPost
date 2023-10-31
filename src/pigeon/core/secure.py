import socket
import ssl
from pigeon.utils.logger import create_log, COLORS

log = create_log('SSL', 'red')


def make_secure(sock, cert_path, privkey_path, privkey_passwd):
    """
    Tries securing a socket to enable HTTPS
    """
    if not privkey_path:
        privkey_passwd = _ask_passwd

    # ssl context for wrapping socket (tls)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        log(3, f'LOADING CERTIFICATE FROM {cert_path}')
        ssl_context.load_verify_locations(cert_path)
        log(3, f'LOADING PRIVATE KEY FROM {privkey_path}')
        ssl_context.load_cert_chain(certfile=cert_path, keyfile=privkey_path, password=privkey_passwd)
    except FileNotFoundError:
        log(0, 'CERTIFICATE_PATH OR PRIVATE_KEY_PATH INVALID!', bypass=True)
        log(0, 'FAILED TO SECURE SOCKET', bypass=True)
        return None
    secure_sock = ssl_context.wrap_socket(sock, server_side=True)
    return secure_sock


def _ask_passwd():
    """
    If the private key is encrypted and no decryption password is provided,
    the user will be prompted to enter it manually.
    """
    log(0, 'COULD NOT DECRYPT PRIVATE KEY')
    passwd = input(COLORS['red'] + 'PRIVATE KEY: ' + COLORS['white'])
    return passwd
