import socket
import pigeon.conf.settings as _settings
from pigeon.utils.logger import create_log
from pigeon.http import HTTPRequest, HTTPResponse
from pigeon.files.static import handle_static_request
from pigeon.files.media import handle_media_request
from pigeon.http.common import error

log = create_log('HANDLER', 'cyan')


def handle_request(client_sock: socket.socket, client_address: tuple):
    log(4, f'TREATING CONNECTION FROM {client_address[0]}:{client_address[1]} as HTTP request')
    settings = _settings.get()

    request = client_sock.recv(4096)

    http_request = HTTPRequest._from_str(str(request, 'ascii'))
    log(4, f'RECEIVED REQUEST:\n{http_request}')
    log(2, f'REQUEST: {http_request.path}')

    # gather response for request
    if settings.static_url_base and http_request.path.startswith(settings.static_url_base):
        # request for static file
        http_response = handle_static_request(http_request)

    elif settings.media_url_base and http_request.path.startswith(settings.media_url_base):
        # request for media file
        http_response = handle_media_request(http_request)

    elif http_request.path in settings.views:
        # views
        http_response = settings.views[http_request.path](http_request)
    else:
        # page does not exist
        http_response = error(404, request)

    client_sock.sendall(http_response.render())

    # close socket
    client_sock.shutdown(socket.SHUT_RDWR)
    client_sock.close()