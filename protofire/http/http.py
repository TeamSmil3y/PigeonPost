import json

class HTTPObject:
    def __init(self, headers):
        self.headers = headers


class HTTPRequest(HTTPObject):
    def __init__(self, method, path, headers, _get='', body={}):
        super().__init__(headers)
        self.method = method
        self.path = path
        self._get = _get
        self.body = body

    def post(key):
        if key not in self.POST: return None
        else: return self.POST[key]

    def get(key):
        if key not in self.GET: return None
        else: return self.GET[key]

    @classmethod
    def from_str(cls, request:str)
        """
            Generates a valid HTTPRequest object from a string representation of the request.
        """


class HTTPResponse(HTTPObject):
    def __init__(self, headers={}, body={})
        super().__init__(headers)
        self.body = body
    
    def render():
        """
            Renders the response into a string that can be sent to the requesting client.
        """
        ...

class JSONRequest(HTTPRequest):
    ...

class JSONResponse(HTTPRequest):
    ...