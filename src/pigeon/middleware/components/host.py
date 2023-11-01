import pigeon.middleware.components as comp
from pigeon.conf import settings
from pigeon.http import HTTPRequest, HTTPResponse


class HostComponent(comp.MiddlewareComponent):
    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest | int:
        if cls.allowed_host(request=request):
            return request
        else:
            return 403

    
    @classmethod
    def allowed_host(cls, request: HTTPRequest) -> bool:
        """
        Checks if the Host header in the request has a valid hostname. 
        """
        return '*' in settings.allowed_hosts or request.headers('host') in settings.allowed_hosts