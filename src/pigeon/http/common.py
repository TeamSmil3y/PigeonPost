import pigeon.conf.settings as _settings
from http import HTTPStatus


def error(code: int, request):
    """
    Returns the HTTPResponse for the error code provided
    """
    settings = _settings.get()

    # if a specific error view for the error code exists
    if code in settings.errors:
        return settings.errors[code](request)
    # otherwise just return a standard error page but with the code provided
    else:
        return settings.errors[000](request, code)


def status(code):
    return str(code) + ' ' + HTTPStatus(code).phrase
