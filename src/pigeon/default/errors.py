from pigeon.http import HTTPResponse, HTTPRequest, JSONResponse


def fallback(request: HTTPRequest | None, code: int):
    """
    Fallback for when no
    """
    return JSONResponse(data={'error': f'error{": " + request.path if request else ""} {code}'}, status=code)
