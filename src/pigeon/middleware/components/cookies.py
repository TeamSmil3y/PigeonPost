from typing import Callable
from pigeon.http import HTTPRequest, HTTPResponse
from typing import Any
from pigeon.utils.common import ParameterDict


class CookieComponent:
    @classmethod
    def preprocess(cls,  request: HTTPRequest) -> HTTPRequest | HTTPResponse:
        """
        Parses cookeis in request and adds them to request object
        """
        if cookie_directives:=request.headers('Cookie'):
            # cookies exist, parse them as defined here (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cookie)
            cookie_pairs = (cookie_directive.split('=') for cookie_directive in cookie_directives.split('; '))
            cookies = ParameterDict({name: value for name,value in cookie_pairs})
            request.cookies = cookies
        else:
            # make cookies empty dict otherwise
            request.cookies = ParameterDict()
        
        return request
