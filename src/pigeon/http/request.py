from pigeon.http.message import HTTPMessage


class HTTPRequest(HTTPMessage):
    def __init__(self, method: str, path: str, headers: dict = None, get: dict = None, data=None, files=None, protocol: str='1.1'):
        """
        Class representing an HTTP request
        """
        super().__init__(headers, data, protocol)
        self.method = method
        self.path = path

        self.GET = get or {}
        self.FILES = files or {}
        
        # set by middleware
        self.is_cors = None
        self.keep_alive = None

    @property
    def is_error(self):
        # A request cannot have a status code and thus neither be a client or server error (response)
        return False

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
