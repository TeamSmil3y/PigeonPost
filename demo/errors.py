from protofire.http.http import JSONResponse
import protofire.http.status as status

def not_found(request):
    return JSONResponse(status=status.get(404), data={'error':'Could not find resource!'})