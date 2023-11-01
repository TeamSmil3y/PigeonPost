import pigeon.middleware.components as comp
from pigeon.http import HTTPRequest, HTTPResponse


class ServerComponent(comp.MiddlewareComponent):
    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse:
        # add server header
        response.set_headers(headers={'Server': 'Pigeon'})
        return response
