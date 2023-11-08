import pigeon.middleware.components as comp
from pigeon.http import HTTPRequest, HTTPResponse


class ConnectionComponent(comp.MiddlewareComponent):
    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse:
        # do not close connection if client requests to keep it alive 
        response.set_headers(headers={'Connection': 'keep-alive' if request.tags.keep_alive else 'close'})
        return response
    
    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest:
        # set keep-alive property for HTTPRequest object
        request.tags.keep_alive = cls.is_keep_alive(request=request)
        return request

    @classmethod
    def is_keep_alive(cls, request: HTTPRequest) -> bool:
        """
        Checks if the Host header in the request has a valid hostname. 
        """
        return request.headers.connection == 'keep-alive'
