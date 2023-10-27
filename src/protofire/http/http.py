import protofire.http.mime as mime

class HttpObject:
    def __init(self, headers):
        self.HEADERS = headers

    def headers(self, key):
        if key not in self.HEADERS:
            return None
        else:
            return self.HEADERS[key]

    @classmethod
    def _parse_headers(cls, headers_str):
        header_lines = headers_str.split('\r\n')

        # parse headers and header params and create 2 dicts from it
        _headers = [_header.split(':', 1) for _header in header_lines[1:]]
        headers = {_header[0].strip():_header[1].split(';')[0].strip() for _header in _headers}
        header_params = {_header[0].strip():(_header[1].split(';'))[1:] for _header in _headers}
        for header, params in header_params.items():
            header_params[header] = {param[0].strip():param[1] for param in [_param.split('=', 1)+[True] for _param in params]}

        return header_lines, headers, header_params


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
    def _from_str(cls, request: str):
        """
            Generates a valid HttpRequest object from a string representation of the request.
        """
        headers_str, body_str = request.split('\r\n\r\n', 1)
        header_lines, headers, header_params = JSONResponse._parse_headers(headers_str)

        # split into method, resource and protocol
        method, resource, protocol = header_lines[0].split(' ')
        # split resource locator into path and get params
        path, _get = resource.split('?')+['']
        # parse get params and create dict from it
        if _get: get = {param[0]:param[1] for param in [_param.split('=', 1) for _param in _get[1:].split('&')]}
        else: get = {}

        if method != 'GET':
            # retrieve parsed body
            body = mime.parse_body(headers['Content-Type'], header_params, body_str)



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
