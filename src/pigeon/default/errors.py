from pigeon.http import HTTPResponse, HTTPRequest, JSONResponse


def fallback(request: HTTPRequest | None, code: int):
    """
    Fallback for when no specific error view is provided for status code
    """
    return JSONResponse(data={'error': f'error{": " + request.path if request else ""} {code}'}, status=code)
