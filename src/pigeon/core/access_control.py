from pigeon.http import HTTPRequest, HTTPResponse
import pigeon.conf.settings as _settings

settings = _settings.get()


def cors_origin_allowed(request: HTTPRequest) -> bool:
    """
    Checks if the Origin header in the request is a valid origin.
    """

    # any origin allowed
    if '*' in settings.cors_allowed_origins:
        return True

    return request.headers('origin') in settings.cors_allowed_origins


def cors_method_allowed(request: HTTPRequest) -> bool:
    """
    Returns true if the 
    """
    return request.method in settings.cors_allow_methods


def cors_credentials_allowed(request: HTTPRequest) -> bool:
    """
    Checks if request has credentials and whether they are allowed as per CORS-policy
    """
    # authentication not implemented yet
    return True


def cors_headers_allowed(request: HTTPRequest) -> bool:
    """
    Checks if the request headers are allowed as per CORS-policy
    """
    return all(header in settings.cors_allow_headers for header in request.HEADERS.data)


def is_cors(request: HTTPRequest) -> bool:
    return request.headers('origin') is not None


def allowed(request: HTTPRequest) -> bool:
    """
    Checks if Origin header and Host header are valid.
    """
    return not is_cors(request) or all((
                cors_origin_allowed(request),
                cors_method_allowed(request),
                cors_headers_allowed(request),
                cors_credentials_allowed(request),
                ))

def get_headers(request: HTTPRequest) -> dict:
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
