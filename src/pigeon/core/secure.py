import ssl
from pigeon.utils.logger import create_log, COLORS

log = create_log('SSL', 'red')


def make_secure(socket, cert_path, privkey_path, privkey_passwd):
    """
        Tries securing a socket to enable HTTPS
    """
    if not privkey_path:
        privkey_passwd = _ask_passwd

    ssl_context = ssl.SSLContext(...)

    raise NotImplementedError


def _ask_passwd():
    """
        If the private key is encrypted and no decryption password is provided,
        the user will be prompted to enter it manually.
    """
    log(0, 'Could not decrypt HTTPS private key')
    passwd = input(COLORS['red'] + 'PRIVATE KEY: ' + COLORS['white'])
    return passwd
