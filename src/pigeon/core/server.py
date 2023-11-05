import socket
from pigeon import Pigeon
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
    if Pigeon.settings.STATIC_FILES_DIR:
        log.info('LOADING STATIC FILES')
        static.load()

    if Pigeon.settings.TEMPLATES_DIR:
        # create jinja2 template environment
        log.info('LOADING TEMPLATES')
        templater.load()


def serve():
    log.info(f'ADDRESS: {Pigeon.settings.ADDRESS if Pigeon.settings.ADDRESS else "ANY"}')
    log.info(f'PORT: {Pigeon.settings.PORT}')

    # open socket
    sock = socket.socket(socket.AF_INET)
    sock.setblocking(False)
    sock.bind((Pigeon.settings.ADDRESS, Pigeon.settings.PORT))

    # configure https if specified in settings
    if Pigeon.settings.USE_HTTPS:
        log.verbose('USING HTTPS')
        secure_sock = secure.make_secure(sock, Pigeon.settings.CERTIFICATE_PATH, Pigeon.settings.PRIVATE_KEY_PATH, Pigeon.settings.PRIVATE_KEY_PASSWD)
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
