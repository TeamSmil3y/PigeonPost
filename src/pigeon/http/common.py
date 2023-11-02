import pigeon.conf
from http import HTTPStatus


def error(code: int, request=None):
    """
    Returns the HTTPResponse for the error code provided
    """
    # if a specific error view for the error code exists
    if code in pigeon.conf.settings.ERRORS:
        return pigeon.conf.settings.ERRORS[code](request=request)
    # otherwise just return a standard error page but with the code provided
    else:
        return pigeon.conf.settings.ERRORS[000](request=request, code=code)


def status(code):
    return str(code) + ' ' + HTTPStatus(code).phrase
