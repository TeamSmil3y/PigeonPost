import protofire.http.parser as parser
import json
import protofire.http.common as common


class HttpObject:
    def __init__(self, headers):
        """
        Parent class for HttpRequest and HttpResponse.
        Implements basic functionality for both HTTP requests and responses. (e.g. headers)
        """
        self.HEADERS: dict[str:str] = headers or {}

    def headers(self, key):
        """
        Returns self.HEADERS[key] if exists else None
        """
        if key not in self.HEADERS:
            return None
        else:
            return self.HEADERS[key]

    def set_headers(self, headers):
        """
        Overwrites headers passed to function
        """
        for header in headers.items():
            self.HEADERS[header[0]] = header[1]


class HttpRequest(HttpObject):
    def __init__(self, method: str, path: str, headers: dict = None, get: dict = None, data=None, files=None):
        """
        Class representing an HTTP request
        """
        super().__init__(headers)
        self.method = method
        self.path = path

        self.GET = get or {}
        self.DATA = data
        self.FILES = files

    def data(self, key):
        """
        Returns self.DATA[key] if exists else None
        """
        # data is list
        if isinstance(self.DATA, (list, tuple)):
            return self.DATA[key] or None
        # data is dict
        elif isinstance(self.DATA, dict):
            return self.DATA.get(key)
        # data is neither dict or list -> access it through object.DATA
        else:
            return None

    def files(self, key):
        """
        Returns self.FILES[key] if exists else None
        """
        # data is list
        if isinstance(self.FILES, (list, tuple)):
            return self.FILES[key] or None
        # data is dict
        elif isinstance(self.FILES, dict):
            return self.FILES.get(key)
        # data is neither dict or list -> access it through object.DATA
        else:
            return None

    def get(self, key):
        """
        Returns self.GET[key] if exists else None
        """
        return self.GET.get(key)

    @classmethod
    def _from_str(cls, request: str):
        """
        Creates a valid HttpRequest object from a string representation of an http request.
        """
        method, path, get, protocol, headers, data, files = parser.parse(request)

        return HttpRequest(method=method, path=path, headers=headers, get=get, data=data, files=files)


class HttpResponse(HttpObject):
    def __init__(self, headers: dict = None, data: str = None, status: int = 200, protocol: str = None):
        """
        Class representing an HTTP response
        """
        super().__init__(headers)
        self.protocol = protocol or "HTTP/1.1"
        self.status = status
        self.data = data or ''

    def render(self):
        """
        Renders the response into a string that can be sent to the requesting client.
        """
        rendered_request_line = bytes(self.protocol + " " + common.status(self.status) + '\r\n', 'ascii')
        if isinstance(self.data, bytes):
            rendered_data = self.data
        else:
            rendered_data = bytes(self.data.replace('\n', '\r\n'), 'ascii')
        self.HEADERS['Content-Length'] = str(len(rendered_data))
        rendered_headers = bytes('\r\n'.join([header[0] + ": " + header[1] for header in self.HEADERS.items()]) + '\r\n\r\n', 'ascii')

        rendered_response = rendered_request_line + rendered_headers + rendered_data
        return rendered_response


class JSONRequest(HttpRequest):
    def __init__(self, **kwargs):
        """
        Not Implemented
        """
        super().__init__(**kwargs)
        raise NotImplementedError


class JSONResponse(HttpResponse):
    def __init__(self, headers: dict = None, data: str = None, status: int = 200, protocol: str = None):
        """
        An HttpResponse but data can be any json convertable python object and the content-type header will be automatically set to application/json.
        """
        super().__init__(headers, data, status, protocol)

        # data is supposed to be json
        self.HEADERS['Content-Type'] = 'application/json'
        self.data = json.dumps(data)
