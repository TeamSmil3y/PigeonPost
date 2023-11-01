import pigeon.middleware.components as comp
from pigeon.conf import settings
from pigeon.http import HTTPRequest, HTTPResponse
from email.utils import formatdate


class DateComponent(comp.MiddlewareComponent):
    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse | int:
        # set date header in response
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        response.set_headers(headers={'Date': date if request.keep_alive else 'close'})
        return response


    @classmethod
    def allowed_host(cls, request: HTTPRequest) -> bool:
        """
        Checks if the Host header in the request has a valid hostname. 
        """
        return '*' in settings.allowed_hosts or request.headers('host') in settings.allowed_hosts