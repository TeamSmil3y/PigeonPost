import pigeon.middleware.components as comp
from pigeon.conf import Manager
from pigeon.http import HTTPRequest, HTTPResponse, error


class MethodComponent(comp.MiddlewareComponent):
    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest | HTTPResponse:
        """
        Checks if the HTTP method in the request is allowed. 
        """
        if cls.allowed_method(request=request):
            return request
        else:
            return error(405)
    
    @classmethod
    def allowed_method(cls, request: HTTPRequest) -> bool:
        return '*' in Manager.allowed_methods or request.method in Manager.allowed_methods
    