from pigeon.http import HTTPRequest, HTTPResponse


class MiddlewareComponent:
    """
    Middleware component that can be used by a preprocessor or postprocessor to process requests.
    """
    @classmethod
    def preprocess(cls,  request: HTTPRequest) -> HTTPRequest | int:
        raise NotImplementedError

    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse | int:
        raise NotImplementedError
    