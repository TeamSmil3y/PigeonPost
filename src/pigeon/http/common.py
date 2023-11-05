<<<<<<< HEAD
import pigeon.conf
from pigeon.middleware.registry import error_handler
=======
from pigeon import Pigeon
>>>>>>> 03e0f9c (:construction::wrench:)
from http import HTTPStatus
from pigeon.http import HTTPResponse, HTTPRequest


def error(code: int, request: HTTPRequest | None = None) -> HTTPResponse | str:
    """
    Returns the HTTPResponse for the error code provided, request parameter optional
    """
<<<<<<< HEAD
    return error_handler(code, request)
=======
    # if a specific error view for the error code exists
    if code in Pigeon.settings.ERRORS:
        return Pigeon.settings.ERRORS[code](request=request)
    # otherwise just return a standard error page but with the code provided
    else:
        return Pigeon.settings.ERRORS[000](request=request, code=code)
>>>>>>> 03e0f9c (:construction::wrench:)


def status(code):
    return str(code) + ' ' + HTTPStatus(code).phrase
