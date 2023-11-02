import pigeon.middleware.components as comp
from pigeon.conf import settings
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
        return '*' in settings.ALLOWED_HOSTS or request.headers('host') in settings.ALLOWED_HOSTS