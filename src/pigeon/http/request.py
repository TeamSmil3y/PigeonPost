from pigeon.http.message import HTTPMessage
from pigeon.utils.common import ParameterDict


class HTTPRequest(HTTPMessage):
    def __init__(self, method: str, path: str, headers: dict = None, get: dict = None, data=None, files=None, protocol: str='1.1', content_type=None):
        """
        Class representing an HTTP request
        """
        super().__init__(headers, data, protocol, content_type)
        self.method = method
        self.path = path

        self.get = ParameterDict(get or None)
        self.files = ParameterDict(get or None)

        # credentials (or other auth related) send in request
        self.auth = None

    @property
    def is_error(self):
        # A request cannot have a status code and thus neither be a client or server error (response)
        return False

