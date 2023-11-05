from typing import Any
from pigeon.http.message import HTTPMessage
import pigeon.http.common as common
import json


class HTTPResponse(HTTPMessage):
    def __init__(self, headers: dict = None, data: str = None, status: int = 200, content_type=None, protocol: str = '1.1'):
        """
        Class representing an HTTP response
        """
        headers = headers or dict()
        super().__init__(headers, data, protocol)
        self.status = status

        if content_type:
            self.HEADERS['Content-Type'] = content_type

        # set by middleware
        self.is_cors = None

    @property
    def is_error(self):
        return self.status >= 400

    def render(self):
        """
        Renders the response into a string that can be sent to the requesting client.
        """
        rendered_request_line = bytes('HTTP/1.1' + " " + common.status(self.status) + '\r\n', 'ascii')
        
        if isinstance(self.DATA, bytes):
            rendered_data = self.DATA
        else:
            rendered_data = bytes(self.DATA.replace('\n', '\r\n'), 'ascii')
            
        self.HEADERS['Content-Length'] = str(len(rendered_data))
        rendered_headers = self.HEADERS.render()

        rendered_response = rendered_request_line + rendered_headers + rendered_data
        return rendered_response


class JSONResponse(HTTPResponse):
    def __init__(self, headers: dict = None, data: Any = None, status: int = 200, protocol: str = '1.1'):
        """
        An HTTPResponse but data can be any json convertable python object and the content-type header will be automatically set to application/json.
        """
        super().__init__(headers=headers, data=json.dumps(data), status=status, protocol=protocol)

        # data is supposed to be json
        self.HEADERS['Content-Type'] = 'application/json'
