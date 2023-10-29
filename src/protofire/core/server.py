import socket
import protofire.conf.settings as _settings
import protofire.core.secure as secure
from protofire.utils.logger import create_log
import protofire.core.handler as handler
import protofire.default.errors as default_errors
import protofire.files.static as static

log = create_log('SERVER', 'white')
global settings


def start(settings_used: _settings.Settings):
    log(2, 'STARTING SERVER...')
    _settings.use(settings_used)
    global settings
    settings = settings_used

    # apply default settings if not overwritten
    settings.errors = default_errors.errors.update(settings.errors)

    # load static files into memory
    log(2, 'LOADING STATIC FILES')
    static.load()

    serve()

def serve():
    global settings
    log(3, f'ADDRESS: {settings.address[0] if settings.address[0] else "ANY"}')
    log(3, f'PORT: {settings.address[1]}')

    # open socket
    sock = socket.socket(socket.AF_INET)
    sock.bind(settings.address)

    # configure https if specified in settings
    if settings.use_https:
        log(3, 'USING HTTPS')
        secure_sock = secure.make_secure(sock, settings.https_cert_path, settings.https_privkey_path,
                                         settings.https_privkey_passwd)

    # listen for incoming connections and then forward them to the handler
    sock.listen()
    try:
        while True:
            client_sock, client_address = sock.accept()
            log(4, f'CONNECTION FROM {client_address[0]}:{client_address[1]}')
            handler.handle_request(client_sock, client_address)

    # close socket on user exit
    except KeyboardInterrupt:
        log(2, 'EXITING', prefix='\n')
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()


if __name__ == '__main__':
    start(_settings.Settings(
        '',
        80,
        {},
        {},
    ))
