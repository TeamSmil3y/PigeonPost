import socket
import pigeon.conf.settings as _settings
import pigeon.core.access_control as access_control
from pigeon.utils.logger import create_log
from pigeon.http import HTTPRequest, HTTPResponse
from pigeon.files.static import handle_static_request
from pigeon.files.media import handle_media_request
from pigeon.http.common import error
import threading

log = create_log('HANDLER', 'cyan')
settings = _settings.get()


def get_response(request) -> HTTPResponse:
    """
    Gathers response for request
    """

    # gather response for request
    if settings.static_url_base and request.path.startswith(settings.static_url_base):
        # request for static file
        response = handle_static_request(request)

    elif settings.media_url_base and request.path.startswith(settings.media_url_base):
        # request for media file
        response = handle_media_request(request)

    elif request.path in settings.views:
        # views
        response = settings.views[request.path](request)
    else:
        # page does not exist
        return error(404, request)

    # invalid request
    if not access_control.allowed(request):
        response = error(403, request)

    # add access-control headers
    if access_control.is_cors(request):
        response.set_headers(access_control.get_headers(request))

    return response


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
        request = HTTPRequest.from_str(str(data, 'ascii'))
        log(2, f'REQUEST: {request.path}')

        # gather appropriate response for request
        response = get_response(request)

        # send response to client
        log(3, f'SENDING RESPONSE TO {client_address[0]}:{client_address[1]}')
        client_sock.sendall(response.render())
        log(3, f'RESPONSE SENT')

        # client asks to terminate connection
        if request.headers('connection') == 'close':
            log(4, f'CLOSING CONNECTION TO {client_address[0]}:{client_address[1]}')
            break

    # close socket
    log(3, f'CLOSING CONNECTION FROM {client_address[0]}:{client_address[1]}')
    client_sock.shutdown(socket.SHUT_RDWR)
    client_sock.close()
