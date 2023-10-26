import json
import protofire.http.mime

class HttpObject:
    def __init(self, headers):
        self.HEADERS = headers

    def headers(self, key):
        if key not in self.HEADERS:
            return None
        else:
            return self.HEADERS[key]


class HttpRequest(HttpObject):
    def __init__(self, method: str, path: str, headers: dict = {}, _get: str = '', _post: str = '', _put = ''):
        super().__init__(headers)
        self.method = method
        self.path = path
        self._get = _get
        self._post = _post
        self._put = _put

        self.GET = {}
        self.POST = {}
        
        self._gen_method_arrays()

    def post(self, key):
        if key not in self.POST:
            return None
        else:
            return self.POST[key]

    def get(self, key):
        if key not in self.GET:
            return None
        else:
            return self.GET[key]
        
    def _gen_method_arrays(self):
        # GET dict
        self.GET = {param[0]:param[1] for param in [_param.split('=') for _param in self._get[1:].split('&')]}

        # POST dict
        if self.method == 'POST':
            match(self.headers('Content-Type')):
                case 'application':
                    ...

        if self.method == 'PUT':
            self.PUT = self._put

    @classmethod
    def from_str(cls, request: str):
        """
            Generates a valid HttpRequest object from a string representation of the request.
        """



class HttpResponse(HttpObject):
    def __init__(self, headers: dict = {}, body: dict = {}):
        super().__init__(headers)
        self.body = body

    def render(self):
        """
            Renders the response into a string that can be sent to the requesting client.
        """
        ...


class JSONRequest(HttpRequest):
    ...


class JSONResponse(HttpResponse):
    ...
