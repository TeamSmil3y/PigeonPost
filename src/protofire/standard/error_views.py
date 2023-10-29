from protofire.http.http import  HttpResponse, HttpRequest, JSONResponse
import protofire.http.status as status


def std(request: HttpRequest, code: int):
    return JSONResponse(data={'error':f'invalid request: {request.path}'}, status=status.get(code))