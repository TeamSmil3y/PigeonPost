from pigeon.http import  HTTPResponse, HTTPRequest, JSONResponse


def fallback(request: HTTPRequest, code: int):
    """
    Fallback for when no
    """
    return JSONResponse(data={'error':f'invalid request: {request.path}'}, status=code)
