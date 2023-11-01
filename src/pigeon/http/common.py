from pigeon.conf import settings
from http import HTTPStatus


def error(code: int, request):
    """
    Returns the HTTPResponse for the error code provided
    """
    # if a specific error view for the error code exists
    if code in settings.errors:
        return settings.errors[code](request=request)
    # otherwise just return a standard error page but with the code provided
    else:
        return settings.errors[000](request=request, code=code)


def status(code):
    return str(code) + ' ' + HTTPStatus(code).phrase
