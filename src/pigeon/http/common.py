import pigeon.conf
from pigeon.middleware.registry import error_handler
from http import HTTPStatus
from pigeon.http import HTTPResponse, HTTPRequest


def error(code: int, request: HTTPRequest | None = None) -> HTTPResponse | str:
    """
    Returns the HTTPResponse for the error code provided, request parameter optional
    """
    return error_handler(code, request)


def status(code):
    return str(code) + ' ' + HTTPStatus(code).phrase
