import pigeon.middleware.components as comp
from pigeon.http import HTTPRequest, HTTPResponse
from email.utils import formatdate


class DateComponent(comp.MiddlewareComponent):
    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse:
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        response.set_headers(headers={'Date': date})
        return response
