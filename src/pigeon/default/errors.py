from pigeon.http.response import HTTPResponse
from pigeon.http.request import HTTPRequest
import json


def fallback(request: HTTPRequest | None, code: int):
    """
    Fallback for when no specific error view is provided for status code
    """
    return HTTPResponse(data=json.dumps({'error': f'error{": " + request.path if request else ""} {code}'}), content_type='application/json', status=code)
