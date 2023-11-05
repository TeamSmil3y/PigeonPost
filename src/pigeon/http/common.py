from pigeon.conf import Manager
from http import HTTPStatus
from pigeon.http.response import HTTPResponse
from pigeon.http.request import HTTPRequest


def error(code: int, request: HTTPRequest | None = None) -> HTTPResponse | str:
    """
    Returns the HTTPResponse for the error code provided, request parameter optional
    """
    return Manager.error_handler(code, request)


def status(code):
    return str(code) + ' ' + HTTPStatus(code).phrase
