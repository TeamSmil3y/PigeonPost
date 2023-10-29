from protofire.http.http import JSONResponse

def welcome(request):
    return JSONResponse(data={'welcome':'Hello World!'})