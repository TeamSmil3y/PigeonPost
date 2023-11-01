from pigeon.utils.logger import create_log
from pigeon.conf import settings
from pigeon.files import handle_media_request, handle_static_request
from pigeon.http import HTTPRequest, HTTPResponse, error
import pigeon.conf.middleware as middleware
import pigeon.middleware.processing as processing
import pigeon.http.parsing.parser as parser

log = create_log('MIDDLEWARE', 'green')



def preprocess(raw: str) -> HTTPRequest | int:
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
        return processing.PROCESSORS[request.protocol].preprocess(request=request)
    except Exception:
        log(1, f'MIDDLEWARE FAILED WHEN PREPROCESSING REQUEST - SKIPPING')
        return 500


def process(request: HTTPRequest | int) -> HTTPResponse:
    """
    Gathers the response from the application logic.
    """
    
    # if request is of type integer, the preprocessing failed and an error should be returned
    if isinstance(request, int):
        # request failed - return error to client
        return error(request, None)

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

    return response
    

def postprocess(request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
    """
    Modifies some components of the response such as headers to fit in with server-side policies (e.g. CORS).
    """
    
    # if preprocessor failed response cannot reliably be postprocessed
    if isinstance(request, int):
        return response
    
    # try processing the request
    try:
        return processing.PROCESSORS[request.protocol].postprocess(response=response, request=request)
    except Exception:
        log(1, f'MIDDLEWARE FAILED WHEN POSTPROCESSING REQUEST - SKIPPING')
        return 500
