import protofire.conf.settings as _settings
from protofire.http.http import HttpRequest, HttpResponse

def error(code: int, request: HttpRequest):
    """
    Returns the HttpResponse for the error code provided
    """
    settings = _settings.get()
    
    # if a specific error view for the error code exists
    if code in settings.error_views:
        return settings.error_views[code](request)
    # otherwise just return a standard error page but with the code provided
    else:
        return settings.error_views[000](request, code)