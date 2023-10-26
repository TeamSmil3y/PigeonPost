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
    def __init__(self, method: str, path: str, headers: dict = {}, get: str = '', post: str = '', put = ''):
        super().__init__(headers)
        self.method = method
        self.path = path

        self.GET = get
        self.POST = post
        self.PUT = put
        
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

    @classmethod
    def from_str(cls, request: str):
        """
            Generates a valid HttpRequest object from a string representation of the request.
        """
        header_lines = request[:request.index('\r\n\r\n')].split('\r\n')
        method, resource, protocol = header_lines[0].split(' ')
        path, _get = resource.split('?')+['']
        get = {param[0]:param[1] for param in [_param.split('=', 1) for _param in _get[1:].split('&')]}
        headers = {header[0].strip():header[1].strip() for header in [_header.split(':', 1) for _header in header_lines[1:]]}
        ...



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
