import protofire.http.mime as mime

class HttpObject:
    def __init__(self, headers):
        self.HEADERS = headers

    def headers(self, key):
        if key not in self.HEADERS:
            return None
        else:
            return self.HEADERS[key]


class HttpRequest(HttpObject):
    def __init__(self, method: str, path: str, headers: dict = {}, get: str = '', post='', put=''):
        super().__init__(headers)
        self.method = method
        self.path = path

        self.GET = get
        self.POST = post
        self.PUT = put
        
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
    def _from_str(cls, request: str):
        """
            Generates a valid HttpRequest object from a string representation of the request.
        """
        request_line, request_headers_body = request.split('\r\n', 1)
        headers, body = mime.parse_raw(request_headers_body)


        # split into method, resource and protocol
        method, resource, protocol = request_line.split(' ')
        # split resource locator into path and get params
        path, get_raw = resource.split('?')+['']
        # parse get params and create dict from it
        if get_raw: get = {param[0]:param[1] for param in [_param.split('=', 1) for _param in get_raw[1:].split('&')]}
        else: get = {}

        return HttpRequest(method=method, path=path, headers=headers, get=get, post=body, put='')



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
