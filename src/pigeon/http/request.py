from pigeon.http.message import HTTPMessage
from pigeon.http.parser import parse

class HTTPRequest(HTTPMessage):
    def __init__(self, method: str, path: str, headers: dict = None, get: dict = None, data=None, files=None):
        """
        Class representing an HTTP request
        """
        super().__init__(headers, data)
        self.method = method
        self.path = path

        self.GET = get or {}
        self.FILES = files or {}
        
    def files(self, key):
        """
        Returns self.FILES[key] if exists else None
        """
        return self.FILES.get(key)
        
    def get(self, key):
        """
        Returns self.GET[key] if exists else None
        """
        return self.GET.get(key)
    
    @classmethod
    def _from_str(cls, request: str):
        """
        Creates a valid HTTPRequest object from a string representation of an http request.
        """
        method, path, get, protocol, headers, data, files = parse(request)

        return HTTPRequest(method=method, path=path, headers=headers, get=get, data=data, files=files)
