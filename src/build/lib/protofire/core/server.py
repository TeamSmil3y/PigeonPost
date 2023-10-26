import socket
from protofire.utils.settings import Settings
import protofire.utils.secure as secure
from protofire.utils.logger import create_log
from protofire.core.handler import handle_request

log = create_log('SERVER', 'white')


def run(settings: Settings):
    log(2, 'STARTING SERVER...')
    log(3, f'ADDRESS: {settings.address[0] if settings.address[0] else "ANY"}')
    log(3, f'PORT: {settings.address[1]}')

    sock = socket.socket(socket.AF_INET)
    sock.bind(settings.address)

    if settings.use_https:
        log(3, 'USING HTTPS')
        secure_sock = secure.make_secure(sock, settings.https_cert_path, settings.https_privkey_path, settings.https_privkey_passwd)

    sock.listen()
    try:
        while True:
            client_sock, client_address = sock.accept()
            log(4, f'CONNECTION FROM {client_address[0]}:{client_address[1]}')
            handle_request(client_sock, client_address)

    except KeyboardInterrupt:
        log(2, 'EXITING', prefix='\n')
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()


if __name__ == '__main__':
    run(Settings(
        '',
        80,
        {},
        {},
    ))
