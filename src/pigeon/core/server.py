import socket
from pigeon.conf import settings
import pigeon.conf as conf
from pigeon.utils.logger import create_log
import pigeon.core.secure as secure
import pigeon.core.handler as handler
import pigeon.files.static as static
import pigeon.templating.templater as templater
import threading

log = create_log('SERVER', 'white')


def start(settings_used):
    # configure settings
    conf.manager.override(settings_used)
    conf.manager.setup()

    log(2, 'STARTING SERVER...')

    # load static files into memory
    if settings.STATIC_FILES_DIR:
        log(2, 'LOADING STATIC FILES')
        static.load()

    if settings.TEMPLATES_DIR:
        # create jinja2 template environment
        log(2, 'LOADING TEMPLATES')
        templater.load()

    serve()


def serve():
    log(2, f'ADDRESS: {settings.ADDRESS if settings.ADDRESS else "ANY"}')
    log(2, f'PORT: {settings.PORT}')

    # open socket
    sock = socket.socket(socket.AF_INET)
    sock.setblocking(False)
    sock.bind((settings.ADDRESS, settings.PORT))

    # configure https if specified in settings
    if settings.USE_HTTPS:
        log(3, 'USING HTTPS')
        secure_sock = secure.make_secure(sock, settings.CERTIFICATE_PATH, settings.PRIVATE_KEY_PATH, settings.PRIVATE_KEY_PASSWD)
        # securing socket failed
        if not secure_sock:
            log(0, 'HTTPS FAILED')
            exit(-1)

        sock = secure_sock

    # listen for incoming connections and then forward them to the handler
    sock.listen()

    try:
        while True:
            log(4, f'WAITING FOR CONNECTIONS')

            # receive client connection
            client_sock = None
            while not client_sock:
                try:
                    client_sock, client_address = sock.accept()
                except BlockingIOError:
                    pass


            log(3, f'CONNECTION FROM {client_address[0]}:{client_address[1]}')
            threading.Thread(target=handler.handle_connection, args=(client_sock, client_address)).start()

    # user exit - close socket
    except KeyboardInterrupt:
        log(2, 'EXITING', prefix='\n')
        log(1, 'APPLICATION WILL EXIT ONCE THREADS HAVE BEEN TERMINATED')
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
