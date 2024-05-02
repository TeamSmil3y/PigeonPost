import socket
import sys
import pigeon.middleware as middleware
import pigeon.utils.logger as logger
from pigeon.http import HTTPRequest, HTTPResponse

log = logger.Log('HANDLER', 'cyan')


def receive_data(client_sock: socket.socket, size: int = 4096) -> bytes:
    while True:
        try:
            return client_sock.recv(size)
        except BlockingIOError:
            pass


def handle_connection(client_sock: socket.socket, client_address: tuple) -> None:
    """
    Takes a connection, gathers correct response and returns it to client.
    """
    log.verbose(f'TREATING CONNECTION FROM {client_address[0]}:{client_address[1]} as HTTP request')

    # set socket to be non-blocking
    client_sock.setblocking(False)

    # receive raw requests until no data is received
    while True:
        log.debug(f'RECEIVING REQUEST FROM {client_address[0]}:{client_address[1]}')

        # receive data from client
        data = receive_data(client_sock=client_sock)

        # client terminated connection
        if not data:
            log.debug(f'CONNECTION TO {client_address[0]}:{client_address[1]} LOST')
            return

        log.debug(f'RAW PACKET:\n{data}')

        try:

            # parse request into HTTPRequest
            request = middleware.preprocess(data)
            if isinstance(request, HTTPRequest):
                log.info(f'REQUEST: {request.path}')

            # gather appropriate response for request
            response = middleware.process(request)
            response = middleware.postprocess(request, response)

            # send response to client
            log.verbose(f'SENDING RESPONSE TO {client_address[0]}:{client_address[1]}')
            client_sock.sendall(response.__bytes__('ascii'))
            log.verbose(f'RESPONSE SENT')

        except Exception as e:
            sys.excepthook(None, e, None, custom_log=log, description=f'EXCEPTION OCCURED WHILE HANDLING REQUEST FROM {client_address[0]}:{client_address[1]}')

        # do not keep connection open on error
        if response.is_error:
            break

        # client asks to terminate connection
        if not request.tags.keep_alive:
            log.debug(f'CLOSING CONNECTION TO {client_address[0]}:{client_address[1]}')
            break

    # close socket
    log.verbose(f'CLOSING SOCKET')
    client_sock.shutdown(socket.SHUT_RDWR)
    client_sock.close()
