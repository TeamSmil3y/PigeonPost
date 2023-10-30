from pigeon.http import JSONResponse
from pigeon.http.common import status

def not_found(request):
    return JSONResponse(status=404, data={'error':'Could not find resource!'})