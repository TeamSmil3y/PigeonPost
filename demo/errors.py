from protofire.http import JSONResponse
from protofire.http.common import status

def not_found(request):
    return JSONResponse(status=404, data={'error':'Could not find resource!'})