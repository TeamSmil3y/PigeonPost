import sys
import pigeon.utils.logger as logger
from pigeon.http.message import HTTPMessage
from pigeon.http import HTTPRequest, HTTPResponse, error
import pigeon.conf.middleware as middleware
import pigeon.middleware.conversion.converter as converter
from pigeon.middleware.tags import MiddlewareTags

log = logger.Log('MIDDLEWARE', 'green')


def preprocess(raw: bytes) -> HTTPResponse | HTTPRequest:
    """
    Tries to parse the raw request and checks whether the request is valid.
    If the request is invalid or could not be parsed correctly, an http error response will be returned.
    """
    log.debug(f'PREPROCESSING REQUEST...')
    
    # try parsing the request
    try:
        request: HTTPRequest = converter.parse(raw)
    except Exception as e:
        sys.excepthook(None, e, None, custom_log=log, description='COULD NOT PARSE REQUEST - SKIPPING')
        return error(400)
    
    if request.protocol not in middleware.HTTP_VERSIONS:
        # server doesn't understand protocol
        log.warning(f'RECEIVED REQUEST OF UNKNOWN PROTOCOL VERSION - SKIPPING')
        return error(505)
    
    # try processing the request
    try:
        request.tags = MiddlewareTags()
        return middleware.PROCESSORS[request.protocol].preprocess(request=request)
    except Exception as e:
        sys.excepthook(None, e, None, custom_log=log, description='MIDDLEWARE FAILED WHEN PREPROCESSING REQUEST - SKIPPING')
        return error(500)


def process(message: HTTPMessage) -> HTTPResponse:
    """
    Gathers the response from the application logic.
    """
    log.debug(f'PROCESSING REQUEST...')
    
    # check if preprocessor retured an error
    if message.is_error:
        log.info(f'PREPROCESSOR RETURNED ERROR {message.status}')
        # request failed preprocessing - return error to client
        # do not further process request
        return message

    # process request
    try:
        response = middleware.PROCESSORS[message.protocol].process(request=message)
    except Exception as e:
        sys.excepthook(None, e, None, custom_log=log, description='VIEW RAISED EXCEPTION')
        response = error(500)

    # if processor returned an error log it
    if response.is_error:
        log.warning(f'PROCESSOR RETURNED ERROR {response.status}')

    return response


def postprocess(message: HTTPMessage, response: HTTPResponse) -> HTTPResponse:
    """
    Modifies some components of the response such as headers to fit in with server-side policies (e.g. CORS).
    """
    log.debug(f'POSTPROCESSING REQUEST..')
    
    # if preprocessor returned an error return the error from the processor to client
    if message.is_error:
        return response
    # if preprocessor hasn't returned an error it is required to return a valid HTTPRequest object
    request = message
    
    # try processing the request
    try:
        response = middleware.PROCESSORS[request.protocol].postprocess(response=response, request=request)
        # request failed postprocessing - return error to client
        return response
    except Exception as e:
        sys.excepthook(None, e, None, custom_log=log, description='MIDDLEWARE FAILED WHEN POSTPROCESSING REQUEST - SKIPPING')
        return error(code=500, request=request)
