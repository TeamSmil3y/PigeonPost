from protofire.http.http import  HttpResponse, HttpRequest, JSONResponse
import protofire.http.status as status


def fallback(request: HttpRequest, code: int):
    """
    Fallback for when no
    """
    return JSONResponse(data={'error':f'invalid request: {request.path}'}, status=status.get(code))


errors = {
    000: fallback,
}