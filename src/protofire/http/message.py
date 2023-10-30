import collections


class HTTPHeaders(collections.UserDict):
    def __init__(self, headers=None):
        data = headers or dict()
        super().__init__(data)

    def __add__(self, other):
        if not isinstance(other, (HTTPHeaders, dict)):
            raise ValueError
        return HTTPHeaders(
            headers=dict(**self.data, **other.data)
        )
        
    def render(self):
        """
        Render headers to a bytes-like object.
        """
        return bytes('\r\n'.join([header[0] + ": " + header[1] for header in self.data.items()]) + '\r\n\r\n', 'ascii')
    

class HTTPMessage:
    def __init__(self, headers, data):
        self.HEADERS: HTTPHeaders = headers if isinstance(headers, HTTPHeaders) else HTTPHeaders(headers=headers)
        self.DATA = data

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
