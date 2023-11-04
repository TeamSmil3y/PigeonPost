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
        # if no mimetype is available for a view, it does not exist:
        if not settings.VIEWHANDLER.get_available_mimetypes(request.path):
            return request, callback
        
        # view exists
        request.tags.is_view_request = True
        typed_callback = cls.negotiate_func(request)
        # could not find typed view fitting view
        if not typed_callback:
            # return request and lambda for error
            return request, lambda request: error(406)
        # return view
        return request, typed_callback

    @classmethod
    def negotiate_func(cls, request):
        """
        Returns exsiting acceptable view for request.
        Since untyped views are assigned the mimetype */* at runtime and are often used as a fallback,
        if no content type is found, they will only be returned if no other matching mimetype is found.
        """
        # get available mimetypes for view
        view_handler = settings.VIEWHANDLER
        available_mimetypes = tuple(mimetype.split('/') for mimetype in view_handler.get_available_mimetypes(request.path))
        
        # get mimetype from request and then cross-check with available mimetypes
        for mimetype in request.accept:
            # get top-level-mimetype and subtype from content_type
            mimetype, subtype = mimetype.split('/')

            for available_mimetype, available_subtype in available_mimetypes:
                # mimetype match
                if mimetype == available_mimetype and subtype == '*' or subtype == available_subtype or available_subtype == '*':
                    return view_handler.get_func(request.path, available_mimetype+'/'+available_subtype)

        # return view for any mimetype if it exists
        if '*/*' in available_mimetypes:
            return view_handler.get_func(request.path, '*/*')

        # no macthing mimetype is found
        return None

    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest:
        # skip conment negotiation for now
        request.accept = cls.parse_accept_header(request)
        request.accept_encoding = cls.parse_accept_encoding_header(request)
        return request

    @classmethod
    def parse_header(cls, header: str) -> tuple:
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
