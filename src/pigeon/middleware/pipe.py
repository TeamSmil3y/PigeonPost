from pigeon.utils.logger import create_log
from pigeon.conf import settings
from pigeon.files import handle_media_request, handle_static_request
from pigeon.http import HTTPRequest, HTTPResponse, error
import pigeon.conf.middleware as middleware
import pigeon.http.parsing.parser as parser

log = create_log('MIDDLEWARE', 'green')


def preprocess(raw: bytes) -> HTTPRequest | int:
    """
    Tries to parse the raw request and checks whether the request is valid.
    If the request is invalid or could not be parsed correctly, an http status error code will be returned.
    """
    
    # try parsing the request
    try:
        request: HTTPRequest = parser.parse(raw)
    except Exception:
        log(1, f'COULD NOT PARSE REQUEST - SKIPPING')
        return 400
    
    if request.protocol not in middleware.HTTP_VERSIONS:
        # server doesn't understand protocol
        return 505
    
    # try processing the request
    try:
        return middleware.PROCESSORS[request.protocol].preprocess(request=request)
    except Exception:
        log(1, f'MIDDLEWARE FAILED WHEN PREPROCESSING REQUEST - SKIPPING')
        return 500


def process(request: HTTPRequest | int) -> HTTPResponse:
    """
    Gathers the response from the application logic.
    """
    
    # if request is of type integer, the preprocessing failed and an error should be returned
    if isinstance(request, int):
        log(2, f'PREPROCESSOR RETURNED ERROR {request}')
        # request failed preprocessing - return error to client
        # -> request now contains the http response status code, not the actual request
        return error(code=request, request=None)

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
        return error(code=404, request=request)

    return response
    

def postprocess(request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
    """
    Modifies some components of the response such as headers to fit in with server-side policies (e.g. CORS).
    """
    
    # check if preprocessor exited correctly
    if isinstance(request, int):
        request = None
    
    # try processing the request
    try:
        response = middleware.PROCESSORS[request.protocol].postprocess(response=response, request=request)
        # request failed postprocessing - return error to client
        # -> response now contains the http response status code, not the actual response
        if isinstance(response, int):
            return error(code=response, request=None)
        return response
    except Exception:
        log(1, f'MIDDLEWARE FAILED WHEN POSTPROCESSING REQUEST - SKIPPING')
        return error(code=500, request=request)
