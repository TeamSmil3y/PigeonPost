import socket
import protofire.utils.settings as _settings
from protofire.utils.logger import create_log
from protofire.http.http import HttpRequest, HttpResponse
from protofire.files.static import handle_static_request
from protofire.files.media import handle_media_request

log = create_log('HANDLER', 'cyan')


def handle_request(client_sock: socket.socket, client_address: tuple):
    log(4, f'TREATING CONNECTION FROM {client_address[0]}:{client_address[1]} as HTTP request')
    settings = _settings.get()

    request = client_sock.recv(4096)

    http_request = HttpRequest._from_str(str(request, 'ascii'))
    log(4, f'RECEIVED REQUEST:\n{http_request}')
    print('DATA:', http_request.DATA, 'FILES:', http_request.FILES, '\nHEADERS:', http_request.HEADERS, '\nMETHOD:', http_request.method, '\nPATH:', http_request.path, '\nGET:', http_request.GET)

    # gather response for request
    if settings.static_url_base and http_request.path.startswith(settings.static_url_base):
        # request for static file
        http_response = handle_static_request(http_request)

    elif settings.media_url_base and http_request.path.startswith(settings.media_url_base):
        # request for media file
        http_response = handle_media_request(http_request)

    else:
        # views
        http_response = HttpResponse(headers={"Content-Type": "application/json"} , data="{\"whoami\": \"lstuma\"}", status="200 OK")

    client_sock.sendall(http_response.render())

    # close socket
    client_sock.shutdown(socket.SHUT_RDWR)
    client_sock.close()