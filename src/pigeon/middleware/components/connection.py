import pigeon.middleware.components as comp
from pigeon.conf import settings
from pigeon.http import HTTPRequest, HTTPResponse




class ConnectionComponent(comp.MiddlewareComponent):
    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse | int:
        # do not close connection if client requests to keep it alive 
        if cls.is_keep_alive(request=request):
            response.set_headers(headers={'Connection': 'keep-alive'})
        response.set_headers(headers={'Connection': 'close'})
        return response
    


    @classmethod
    def is_keep_alive(cls, request: HTTPRequest) -> bool:
        """
        Checks if the Host header in the request has a valid hostname. 
        """
        return request.headers('connection') == 'keep-alive'