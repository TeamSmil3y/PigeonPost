import socket
import pigeon.conf.settings as _settings
import pigeon.core.access_control as access_control
from pigeon.utils.logger import create_log
from pigeon.http import HTTPRequest, HTTPResponse
from pigeon.files.static import handle_static_request
from pigeon.files.media import handle_media_request
from pigeon.http.common import error
from pigeon.core.common import sync_to_async

log = create_log('HANDLER', 'cyan')


async def get_response(request):
    """_
    Gathers response for request
    """
    settings = _settings.get()


    # gather response for request
    if settings.static_url_base and request.path.startswith(settings.static_url_base):
        # request for static file
        response = await sync_to_async(handle_static_request)(request)

    elif settings.media_url_base and request.path.startswith(settings.media_url_base):
        # request for media file
        response = await sync_to_async(handle_media_request)(request)

    elif request.path in settings.views:
        # views
        response = await sync_to_async(settings.views[request.path])(request)
    else:
        # page does not exist
        return await sync_to_async(error)(404, request)

    # invalid request
    if not access_control.allowed(request):
        response = await sync_to_async(error)(403, request)

    # add access-control headers
    if access_control.is_cors(request):
        response.set_headers(access_control.get_headers(request))

    return response


async def handle_request(client_sock: socket.socket, client_address: tuple):
    """
    Takes an connection, gathers correct response and returns it to client.
    """
    log(4, f'TREATING CONNECTION FROM {client_address[0]}:{client_address[1]} as HTTP request')
    settings = _settings.get()

    # receive raw request
    raw = client_sock.recv(4096)

    # parse request into HTTPRequest
    request = HTTPRequest.from_str(str(raw, 'ascii'))
    log(2, f'REQUEST: {request.path}')

    response = await get_response(request)

    client_sock.sendall(response.render())

    # close socket
    client_sock.shutdown(socket.SHUT_RDWR)
    client_sock.close()
