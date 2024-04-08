import pigeon.middleware.components as comp
from typing import Callable
from pigeon.conf import Manager
from pigeon.http import HTTPRequest, HTTPResponse, error
import pigeon.middleware.conversion.converter as converter


class ContentNegotiationComponent(comp.MiddlewareComponent):
    """
    Implements content-negotiation as specified for HTTP/1.1 and subsequently HTTP/2.0
    """
    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse:
        # skip conment negotiation for now
        return response
    
    @classmethod
    def process(cls, request: HTTPRequest, func: Callable) -> (HTTPRequest, Callable):
        """
        Will change func to be to a typed view if one esists for the requested path and add automatic type conversion to func.
        """
        # if no mimetype is available for a view, it does not exist:
        if not Manager.view_handler.get_available_mimetypes(request.path):
            return request, func
        
        # view exists
        request.tags.is_view_request = True
        typed_func, func_mimetype = cls.negotiate_func(request)
        # could not find typed view fitting view
        if not typed_func:
            # return request and lambda for error
            return request, lambda request: error(406)

        # automatic type conversion for response (e.g. if user view only returns string)
        def autoconverted_typed_func(request: HTTPRequest) -> HTTPResponse:
            return converter.generate(typed_func(request), func_mimetype)

        return request, autoconverted_typed_func

    @classmethod
    def negotiate_func(cls, request) -> tuple[Callable | None,  str | None]:
        """
        Returns exsiting acceptable view for request.
        Since untyped views are assigned the mimetype */* at runtime and are often used as a fallback,
        if no content type is found, they will only be returned if no other matching mimetype is found.
        """
        # get available mimetypes for view
        available_mimetypes = tuple(mimetype.split('/') for mimetype in Manager.view_handler.get_available_mimetypes(request.path))
        
        # get mimetype from request and then cross-check with available mimetypes
        for mimetype in request.accept:
            # get top-level-mimetype and subtype from content_type
            top_level_mimetype, subtype = mimetype.split('/')

            for available_mimetype, available_subtype in available_mimetypes:
                # mimetype match
                if (top_level_mimetype == available_mimetype or top_level_mimetype == '*' and subtype == '*' or subtype == available_subtype or available_subtype == '*'):
                    return Manager.view_handler.get_func(request.path, available_mimetype+'/'+available_subtype), mimetype

        # no macthing mimetype is found
        return None, None

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
        for directive in directives:
            directive.append('q=1')
            while not directive[1].startswith('q'): directive.pop(1)
        directives.sort(key=lambda directive: float(directive[1].split('=')[1]) if len(directive) > 1 else 1, reverse=True)
        return tuple(directive[0] for directive in directives)
    
    @classmethod
    def parse_accept_header(cls, request: HTTPRequest) -> tuple:
        if header := request.headers.accept:
            return cls.parse_header(header)
        return tuple('*/*')
    
    @classmethod
    def parse_accept_encoding_header(cls, request: HTTPRequest) -> tuple:
        if header := request.headers.accept_encoding:
            return cls.parse_header(header)
        return tuple('*')