import collections
from pigeon.utils.common import LowerParameterDict

class HTTPHeaders(collections.UserDict):
    def __init__(self, headers=None):
        headers = headers or dict()
        data = {header[0].lower(): header[1] for header in headers.items()}

        super().__init__(data)

    @property
    def content_type(self):
        return self.headers('content-type')

    @content_type.setter
    def content_type(self, value):
        self.HEADERS['content-type'] = value

    def __add__(self, other):
        if not isinstance(other, (HTTPHeaders, dict)):
            raise ValueError
        return HTTPHeaders(
            headers=dict(**self.data, **other.data)
        )

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

    def __setitem__(self, key, value):
        return super().__setitem__(key.lower(), value)

    def get(self, key):
        return super().get(key.lower())

    def render(self):
        """
        Render headers to a bytes-like object.
        """
        return bytes('\r\n'.join([header[0] + ": " + header[1] for header in self.data.items()]) + '\r\n\r\n', 'ascii')
    

class HTTPMessage:
    def __init__(self, headers, data, protocol, cookies: dict=None):
        self.HEADERS: HTTPHeaders = headers if isinstance(headers, HTTPHeaders) else HTTPHeaders(headers=headers)
        self.DATA: Any = data
        # protocol used (e.g. 1.0, 1.1, 2.0, ...)
        self.protocol: str = protocol

        # cookies of request
        self.cookies: LowerParameterDict = LowerParameterDict(cookies or dict())

    @property
    def is_error(self):
        raise NotImplementedError

    def data(self, key):
        """
        Returns self.DATA[key] if exists else None
        """
        if isinstance(self.DATA, dict):
            return self.DATA.get(key)
        else:
            return None
        
    def set_headers(self, headers):
        """
        Overwrites headers passed to function
        """
        for header in headers.items():
            self.HEADERS[header[0]] = header[1]
        
    def headers(self, key):
        """
        Returns self.HEADERS[key] if exists else None
        """
        return self.HEADERS.get(key)
    
    def render(self):
        raise NotImplementedError
