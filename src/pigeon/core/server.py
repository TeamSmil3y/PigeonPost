import socket
from pigeon.conf import settings
import pigeon.conf as conf
import pigeon.utils.logger as logger
import pigeon.core.secure as secure
import pigeon.core.handler as handler
import pigeon.files.static as static
import pigeon.templating.templater as templater
import threading

log = logger.Log('SERVER', '#bb88ff')


def start():
    log.info('STARTING...')

    # load static files into memory
    if settings.STATIC_FILES_DIR:
        log.info('LOADING STATIC FILES')
        static.load()

    if settings.TEMPLATES_DIR:
        # create jinja2 template environment
        log.info('LOADING TEMPLATES')
        templater.load()


def serve():
    log.info(f'ADDRESS: {settings.ADDRESS if settings.ADDRESS else "ANY"}')
    log.info(f'PORT: {settings.PORT}')

    # open socket
    sock = socket.socket(socket.AF_INET)
    sock.setblocking(False)
    sock.bind((settings.ADDRESS, settings.PORT))

    # configure https if specified in settings
    if settings.USE_HTTPS:
        log.verbose('USING HTTPS')
        secure_sock = secure.make_secure(sock, settings.CERTIFICATE_PATH, settings.PRIVATE_KEY_PATH, settings.PRIVATE_KEY_PASSWD)
        # securing socket failed
        if not secure_sock:
            log.critical('HTTPS FAILED')
            exit(-1)

        sock = secure_sock

    # listen for incoming connections and then forward them to the handler
    sock.listen()

    try:
        while True:
            log.debug(f'WAITING FOR CONNECTIONS')

            # receive client connection
            client_sock = None
            while not client_sock:
                try:
                    client_sock, client_address = sock.accept()
                except BlockingIOError:
                    pass

            log.verbose(f'CONNECTION FROM {client_address[0]}:{client_address[1]}')
            threading.Thread(target=handler.handle_connection, args=(client_sock, client_address)).start()

    # user exit - close socket
    except KeyboardInterrupt:
        print('\n')
        log.info('EXITING')
        log.warning('APPLICATION WILL EXIT ONCE THREADS HAVE BEEN TERMINATED')
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
