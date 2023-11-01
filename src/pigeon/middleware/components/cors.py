import pigeon.middleware.components as comp
from pigeon.conf import settings
from pigeon.http import HTTPRequest, HTTPResponse




class CORSComponent(comp.MiddlewareComponent):
    @classmethod
    def cors_origin_allowed(cls, request: HTTPRequest) -> bool:
        """
        Checks if the Origin header in the request is a valid origin.
        """
    
        # any origin allowed
        if '*' in settings.cors_allowed_origins:
            return True
    
        return request.headers('origin') in settings.cors_allowed_origins
    
    @classmethod
    def cors_method_allowed(cls, request: HTTPRequest) -> bool:
        """
        Returns true if the 
        """
        return request.method in settings.cors_allow_methods
    
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
        return all(header in settings.cors_allow_headers for header in request.HEADERS.data)
    
    @classmethod
    def is_cors(cls, request: HTTPRequest) -> bool:
        return request.headers('origin') is not None
    
    @classmethod
    def allowed(cls, request: HTTPRequest) -> bool:
        """
        Checks if Origin header and Host header are valid.
        """
        return not request.is_cors or all((
               cls.cors_origin_allowed(request),
               cls.cors_method_allowed(request),
               cls.cors_headers_allowed(request),
               cls.cors_credentials_allowed(request)
                ))
    
    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest | int:
        request.is_cors = cls.is_cors(request)
        
        if not cls.allowed(request):
            return 400
        else:
            return request

    @classmethod
    def get_headers(cls, request: HTTPRequest) -> dict:
        """
        Gets server access-control response headers for request
        """
        headers = {
            'Access-Control-Allow-Credentials': str(settings.cors_allow_creds),
            'Access-Control-Allow-Origin': request.headers('origin'),
            'Access-Control-Allow-Headers': ', '.join(settings.cors_allow_headers),
            'Access-Control-Allow-Methods': ', '.join(settings.cors_allow_methods),
            'Access-Control-Max-Age': str(settings.cors_max_age)
        }

        return headers

    @classmethod
    def postprocess(cls,  response: HTTPResponse, request: HTTPRequest) -> HTTPResponse | int:

        if not request.is_cors:
            return response

        # get default CORS headers
        cors_headers = cls.get_headers(request)
        # add CORS headers to response
        response.set_headers(headers=cors_headers)
        