from typing import Callable
from pigeon.http import HTTPRequest, HTTPResponse


class MiddlewareComponent:
    """
    Middleware component that can be used by a preprocessor or postprocessor to process requests.
    """
    @classmethod
    def preprocess(cls,  request: HTTPRequest) -> HTTPRequest | HTTPResponse:
        raise NotImplementedError

    @classmethod
    def process(cls, request: HTTPRequest, func: Callable) -> (HTTPRequest, Callable):
        pass

    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse:
        raise NotImplementedError
    