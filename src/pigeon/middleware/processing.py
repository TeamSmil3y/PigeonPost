from pigeon.http import HTTPRequest, HTTPResponse, error
import pigeon.conf.middleware as middleware
from pigeon.conf import settings
from pigeon.files import handle_media_request, handle_static_request



class Processor:
    @classmethod
    def preprocess(cls,  request: HTTPRequest) -> HTTPRequest | int:
        raise NotImplementedError
    @classmethod
    def postprocess(cls,  response: HTTPResponse,  request: HTTPRequest) -> HTTPResponse | int:
        raise NotImplementedError


class Owl(Processor):
    """
    Processes requests using the HTTP/1.1 protocol
    """
    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest | int:
        # run every middleware preprocess comnponent on request
        for component in middleware.PREPROCESSING_COMPONENTS:
            request = component.preprocess(request=request)
            # request is an error response and should not be processed further
            if request.is_error:
                return request
        return request
    
    @classmethod
    def process(cls, request: HTTPRequest) -> HTTPResponse:
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

    @classmethod
    def postprocess(cls,  response: HTTPResponse,  request: HTTPRequest) -> HTTPResponse | int:
        # run every middleware postprocess component on response
        for component in middleware.POSTPROCESSING_COMPONENTS:
            response = component.postprocess(response=response, request=request)
            if response.is_error:
                return response
        return response
        

class Raven(Processor):
    """
    Processes requests using the HTTP/2.0 protocol
    """
    pass
