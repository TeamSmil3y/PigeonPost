from protofire.http.http import  HttpResponse, HttpRequest, JSONResponse


def fallback(request: HttpRequest, code: int):
    """
    Fallback for when no
    """
    return JSONResponse(data={'error':f'invalid request: {request.path}'}, status=code)


errors = {
    000: fallback,
}