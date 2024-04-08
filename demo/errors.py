from pigeon import Pigeon
from pigeon.http import HTTPResponse
from pigeon.http.common import status

@Pigeon.error(404)
def not_found(request):
    return HTTPResponse(status=404, data="{'error':'Could not find resource!'}", headers={'content-type':'application/json'})