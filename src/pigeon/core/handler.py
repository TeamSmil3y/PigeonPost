import socket
from pigeon.conf import settings
import pigeon.middleware as middleware
from pigeon.utils.logger import create_log
from pigeon.http import HTTPRequest, HTTPResponse
from pigeon.files.static import handle_static_request
from pigeon.files.media import handle_media_request
from pigeon.http.common import error

log = create_log('HANDLER', 'cyan')



def receive_data(client_sock: socket.socket, size:int = 4096):
    while True:
        try:
            return client_sock.recv(size)
        except BlockingIOError:
            pass


def handle_connection(client_sock: socket.socket, client_address: tuple):
    """
    Takes a connection, gathers correct response and returns it to client.
    """
    log(3, f'TREATING CONNECTION FROM {client_address[0]}:{client_address[1]} as HTTP request')

    # set socket to be non-blocking
    client_sock.setblocking(False)

    # receive raw requests until no data is received
    while True:
        log(4, f'RECEIVING REQUEST FROM {client_address[0]}:{client_address[1]}')

        # receive data from client
        data = receive_data(client_sock=client_sock)

        # client terminated connection
        if not data:
            log(4, f'CONNECTION TO {client_address[0]}:{client_address[1]} LOST')
            return

        log(4, f'RAW PACKET:\n{data}')

        # parse request into HTTPRequest
        request = middleware.preprocess(data)
        if isinstance(request, HTTPRequest):
            log(2, f'REQUEST: {request.path}')

        # gather appropriate response for request
        response = middleware.process(request)
        response = middleware.postprocess(request, response)

        # send response to client
        log(3, f'SENDING RESPONSE TO {client_address[0]}:{client_address[1]}')
        client_sock.sendall(response.render())
        log(3, f'RESPONSE SENT')

        # do not keep connection open on error
        if response.is_error:
            break

        # client asks to terminate connection
        if not request.keep_alive:
            log(4, f'CLOSING CONNECTION TO {client_address[0]}:{client_address[1]}')
            break

    # close socket
    log(3, f'CLOSING CONNECTION FROM {client_address[0]}:{client_address[1]}')
    client_sock.shutdown(socket.SHUT_RDWR)
    client_sock.close()
