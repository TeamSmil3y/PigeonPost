import pigeon.middleware.components as comp
from pigeon.http import HTTPRequest, HTTPResponse


class CacheControlComponent(comp.MiddlewareComponent):
    """
    Implements cache-control as specified for HTTP/1.1 and subsequently HTTP/2.0
    """
    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse | int:
        # depending on content decide if and how long response should be cached
        if request.tags.is_media_request:
            # let browser cache response since media files are heavy on backend and might not change instantly
            response.headers.cache_control = 'public, max-age=600'
        elif request.tags.is_static_request:
            # let browser cache for a longer time since static files aren't meant to be changed often
            response.headers.cache_control = 'public, max-age=1800'
        else:
            # prevent browser from caching since request might be dynamic        
            response.headers.cache_control = 'private, no-store'
            
        return response

    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest:
        return request
    
    @classmethod
    def parse_cache_control(cls, header: str) -> dict:
        """
        Parses the cache-control header and returns the diretives as ...?
        """
        raise NotImplementedError
        directives = tuple((directive.split('=')+['True'])[:2] for directive in header.split(','))
        return {name.strip(): value.strip() for name, value in directives}
