from pigeon.http import HTTPRequest
import pigeon.conf.settings as _settings


def hostname_allowed(request: HTTPRequest):
    """
    Checks if the Host header in the request has a valid hostname. 
    """
    settings = _settings.get()
    
    # any host allowed
    if '*' in settings.allowed_hosts:
        return True
    
    return request.headers('host') in settings.allowed_hosts


def cors_origin_allowed(request: HTTPRequest):
    """
    Checks if the Origin header in the request is a valid origin.
    """
    settings = _settings.get()

    # any origin allowed
    if '*' in settings.cors_allowed_origins:
        return True

    return request.headers('origin') in settings.cors_allowed_origins


def cors_method_allowed(request: HTTPRequest):
    """
    Returns true if the 
    """
    settings = _settings.get()

    return request.method in settings.cors_allow_methods


def cors_credentials_allowed(request: HTTPRequest):
    """
    Checks if request has credentials and whether they are allowed as per CORS-policy
    """
    # authentication not implemented yet
    return True


def cors_headers_allowed(request: HTTPRequest):
    """
    Checks if the request headers are allowed as per CORS-policy
    """
    settings = _settings.get()

    return all(header in settings.cors_allow_headers for header in request.HEADERS.data)


def is_cors(request: HTTPRequest):
    return request.headers('origin') is not None


def allowed(request: HTTPRequest):
    """
    Checks if Origin header and Host header are valid.
    """
    return hostname_allowed(request) and not is_cors(request) \
        or all((cors_origin_allowed(request),
                cors_method_allowed(request),
                cors_headers_allowed(request),
                cors_credentials_allowed(request),
                ))


def get_headers(request: HTTPRequest):
    """
    Gets server access-control response headers for request
    """
    settings = _settings.get()

    headers = {
        'Access-Control-Allow-Credentials': str(settings.cors_allow_creds),
        'Access-Control-Allow-Origin': request.headers('origin'),
        'Access-Control-Allow-Headers': ', '.join(settings.cors_allow_headers),
        'Access-Control-Allow-Methods': ', '.join(settings.cors_allow_methods),
        'Access-Control-Max-Age': str(settings.cors_max_age)
    }

    return headers
