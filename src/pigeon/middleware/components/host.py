import pigeon.middleware.components as comp
from pigeon import Pigeon
from pigeon.http import HTTPRequest, HTTPResponse, error


class HostComponent(comp.MiddlewareComponent):
    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest:
        if cls.allowed_host(request=request):
            return request
        else:
            return error(403)

    @classmethod
    def allowed_host(cls, request: HTTPRequest) -> bool:
        """
        Checks if the Host header in the request has a valid hostname. 
        """
        return '*' in Pigeon.ALLOWED_HOSTS or request.headers('host') in Pigeon.settings.ALLOWED_HOSTS