from pigeon.http import HTTPRequest, HTTPResponse
import pigeon.conf.settings as _settings

settings = _settings.get()


def hostname_allowed(request: HTTPRequest) -> bool:
    """
    Checks if the Host header in the request has a valid hostname. 
    """

    # If host in
    return '*' in settings.allowed_hosts or request.headers('host') in settings.allowed_hosts