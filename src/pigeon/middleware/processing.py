from pigeon.http import HTTPRequest, HTTPResponse, error
import pigeon.conf.middleware as middleware


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
            if isinstance(request, int):
                return request
        return request
    
    @classmethod
    def postprocess(cls,  response: HTTPResponse,  request: HTTPRequest) -> HTTPResponse | int:
        # run every middleware postprocess component on response
        for component in middleware.POSTPROCESSING_COMPONENTS:
            response = component.postprocess(response=response, request=request)
            if isinstance(response, int):
                return response
        return response
        

class Raven(Processor):
    """
    Processes requests using the HTTP/2.0 protocol
    """
    pass
