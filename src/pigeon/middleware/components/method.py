import pigeon.middleware.components as comp
from pigeon.conf import settings
from pigeon.http import HTTPRequest, HTTPResponse




class MethodComponent(comp.MiddlewareComponent):
    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest | int:
        """
        Checks if the HTTP method in the request is allowed. 
        """
        if cls.allowed_method(request=request):
            return request
        else:
            return 405
    
    @classmethod
    def allowed_method(cls, request: HTTPRequest) -> bool:
        return '*' in settings.allowed_methods or request.method in settings.allowed_methods