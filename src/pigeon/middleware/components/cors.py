import pigeon.middleware.components as comp
from pigeon.conf import settings
from pigeon.http import HTTPRequest, HTTPResponse, error


class CORSComponent(comp.MiddlewareComponent):
    @classmethod
    def cors_origin_allowed(cls, request: HTTPRequest) -> bool:
        """
        Checks if the Origin header in the request is a valid origin.
        """
    
        # any origin allowed
        if '*' in settings.CORS_ALLOWED_ORIGINS:
            return True
    
        return request.headers('origin') in settings.CORS_ALLOWED_ORIGINS
    
    @classmethod
    def cors_method_allowed(cls, request: HTTPRequest) -> bool:
        """
        Returns true if the 
        """
        return request.method in settings.CORS_ALLOWED_METHODS
    
    @classmethod
    def cors_credentials_allowed(cls, request: HTTPRequest) -> bool:
        """
        Checks if request has credentials and whether they are allowed as per CORS-policy
        """
        # authentication not implemented yet
        return True
    
    @classmethod
    def cors_headers_allowed(cls, request: HTTPRequest) -> bool:
        """
        Checks if the request headers are allowed as per CORS-policy
        """
        return all(header in settings.CORS_ALLOWED_HEADERS for header in request.HEADERS.data)
    
    @classmethod
    def is_cors(cls, request: HTTPRequest) -> bool:
        return request.headers('origin') is not None
    
    @classmethod
    def allowed(cls, request: HTTPRequest) -> bool:
        """
        Checks if Origin header and Host header are valid.
        """
        return not request.tags.is_cors or all((
               cls.cors_origin_allowed(request),
               cls.cors_method_allowed(request),
               cls.cors_headers_allowed(request),
               cls.cors_credentials_allowed(request)
                ))
    
    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest | HTTPResponse:
        request.tags.cors = cls.is_cors(request)
        
        if not cls.allowed(request):
            return error(400)
        else:
            return request

    @classmethod
    def get_headers(cls, request: HTTPRequest) -> dict:
        """
        Gets server access-control response headers for request
        """
        headers = {
            'Access-Control-Allow-Credentials': str(settings.CORS_ALLOW_CREDS),
            'Access-Control-Allow-Origin': request.headers('origin'),
            'Access-Control-Allow-Headers': ', '.join(settings.CORS_ALLOWED_HEADERS),
            'Access-Control-Allow-Methods': ', '.join(settings.CORS_ALLOWED_METHODS),
            'Access-Control-Max-Age': str(settings.CORS_MAX_AGE)
        }

        return headers

    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse:

        if not request.tags.cors:
            return response

        # get default CORS headers
        cors_headers = cls.get_headers(request)
        # add CORS headers to response
        response.set_headers(headers=cors_headers)
