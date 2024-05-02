import socket
import sys
from pigeon.conf import Manager
import pigeon.utils.logger as logger
import pigeon.core.secure as secure
import pigeon.core.handler as handler
import pigeon.files.static as static
import pigeon.templating.templater as templater
import threading

log = logger.Log('SERVER', '#bb88ff')


def start():
    log.info('...STARTING')

    # load static files into memory
    if Manager.static_files_dir:
        log.info('LOADING STATIC FILES')
        static.load()

    if Manager.templates_dir:
        # create jinja2 template environment
        log.info('LOADING TEMPLATES')
        templater.load()


def serve():
    log.info(f'ADDRESS: {Manager.address if Manager.address else "ANY"}')
    log.info(f'PORT: {Manager.port}')

    # open socket
    sock = socket.socket(socket.AF_INET)
    sock.setblocking(False)
    sock.bind((Manager.address, Manager.port))

    # configure https if specified in settings
    if Manager.use_https:
        log.verbose('USING HTTPS')
        secure_sock = secure.make_secure(sock, Manager.certificate_path, Manager.private_key_path, Manager.private_key_passwd)
        # securing socket failed
        if not secure_sock:
            log.critical('HTTPS FAILED')
            sys.exit(-1, force=True)

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
        log.info('EXITING (USER INTERRUPT)')
        log.warning('APPLICATION WILL EXIT ONCE THREADS HAVE BEEN TERMINATED')
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        sys.exit(0, force=True)
