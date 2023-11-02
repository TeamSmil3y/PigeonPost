import pigeon.middleware.components as comp
from typing import Callable
from pigeon.conf import settings
from pigeon.http import HTTPRequest, HTTPResponse, error


class ContentNegotiationComponent(comp.MiddlewareComponent):
    """
    Implements content-negotiation as specified for HTTP/1.1 and subsequently HTTP/2.0
    """
    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse:
        # skip conment negotiation for now
        return response
    
    @classmethod
    def process(cls, request: HTTPRequest, callback: Callable) -> (HTTPRequest, Callable):
        """
        Will change callback to be to a typed view if one esists for the requested path
        """
        
        # views does not exist
        if request.path not in settings.TYPED_VIEWS:
            return request, callback
        
        # view exists
        request.tags.is_view_request = True
        typed_callback = cls.find_callback(request)
        # could not find typed view fitting view
        if not typed_callback:
            # return request and lambda for error
            return request, lambda request: error(406)
        # return typed view
        return request, typed_callback
            
        
    @classmethod
    def find_callback(cls, request):
        """
        Returns exsiting acceptable content-type for the request.
        """
        available = tuple(mimetype.split('/') for mimetype in settings.TYPED_VIEWS[request.path].keys())
        for content_type in request.accept:
            mimetype, subtype = content_type.split('/')
            for available_mimetype, available_subtype in available:
                if mimetype == '*' or mimetype == available_mimetype and subtype == '*' or subtype == available_subtype:
                    return settings.TYPED_VIEWS[request.path][available_mimetype+'/'+available_subtype]
        # if no content type is negotiable return None
        return None
        

    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest:
        # skip conment negotiation for now
        request.accept = cls.parse_accept_header(request)
        request.accept_encoding = cls.parse_accept_encoding_header(request)
        return request

    @classmethod
    def parse_header(cls, header: str):
        """
        Parses header value of style:
        <value>[;q=<quality_factor>], <value>[;q=<quality_factor>], ...
        """
        directives = [directive.strip().split(';') for directive in header.split(',')]
        directives.sort(key=lambda directive: float(directive[1].split('=')[1]) if len(directive) > 1 else 1, reverse=True)
        return tuple(directive[0] for directive in directives)
    
    @classmethod
    def parse_accept_header(cls, request: HTTPRequest) -> tuple:
        if header := request.headers('Accept'):
            return cls.parse_header(header)
        return tuple('*/*')
    
    @classmethod
    def parse_accept_encoding_header(cls, request: HTTPRequest) -> tuple:
        if header := request.headers('Accept-Encoding'):
            return cls.parse_header(header)
        return tuple('*')