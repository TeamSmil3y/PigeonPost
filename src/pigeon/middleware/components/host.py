import pigeon.middleware.components as comp
from pigeon.conf import Manager
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
        return '*' in Manager.allowed_hosts or request.headers.host in Manager.allowed_hosts