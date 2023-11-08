from typing import Any
from pigeon.http.message import HTTPMessage
import pigeon.http.common as common
import json


class HTTPResponse(HTTPMessage):
    def __init__(self, headers: dict = None, data: str = None, status: int = 200, cookies=None, protocol: str = '1.1', content_type=None):
        """
        Class representing an HTTP response
        """
        super().__init__(headers, data, protocol, content_type)

        # HTTP Response status
        self.status = status


    @property
    def is_error(self):
        return self.status >= 400

    def __str__(self):
        return f'HTTP/{self.protocol} {common.status(self.status)}\r\n{super().__str__()}'

    def __bytes__(self, encoding='ascii'):
        return bytes(f'HTTP/{self.protocol} {common.status(self.status)}\r\n', encoding)+super().__bytes__(encoding)