from pigeon.utils.common import ParameterDict, LowerParameterDict
from typing import Any

class HTTPHeader:
    """
    Single HTTP message header
    """
    def __init__(self, name: str, value: str):
        self.name: str = name
        self._value: Any = value

    @property
    def value(self) -> str:
        return self._value
    @value.setter
    def value(self, value) -> None:
        self._value = value

    def __str__(self) -> str:
        return f'{self.name}: {self.value}\r\n'


class HTTPHeaders:
    """
    Class representing HTTP message headers
    """
    def __init__(self, headers: dict[str, str]=None):
        # transform headers dict to LowerParameterDict[str, HTTPHeader]
        headers = headers or dict()
        headers = {name: HTTPHeader(name, value) for name, value in headers.items()}
        # store in parent class to allow accessing it over self._headers -> otherwise __getattr__ override will break it all
        super().__setattr__('_headers', LowerParameterDict(headers))

    def __getattr__(self, key):
        if header:= self._headers.get(key):
            return header.value
        return None

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getitem__(self, key):
        return self._headers[key].value

    def __setitem__(self, key, value):
        self._headers[key] = HTTPHeader(key.replace('_', '-'), value)

    def items(self):
        return self._headers.items()

    def values(self):
        return self._headers.values()

    def __contains__(self, key):
        return self.__getattr__(key) or None

    def __str__(self):
        return ''.join((str(header) for header in self._headers.values()))+'\r\n'


class HTTPData:
    """
    Class representing HTTP message body data
    """
    def __str__(self) -> str:
        raise NotImplementedError



class HTTPMessage:
    """
    An HTTP message (obv either response or request)
    """
    def __init__(self, headers: dict[str, str], data: str, protocol: str, content_type=None):
        # headers of HTTP message
        self.headers: HTTPHeaders = HTTPHeaders(headers or None)
        if content_type:
            self.headers.content_type = content_type
        # http message body (data)
        self.data: Any = data
        # protocol used (e.g. 1.1, 1.0, 2.0, ...)
        self.protocol: str = protocol

    @property
    def is_error(self):
        raise NotImplementedError

    def set_headers(self, headers):
        """
        Overwrites headers passed to function
        """
        for key, value in headers.items():
            self.headers[key] = value

    def __str__(self):
        # data needs to be string to make accurately render message
        if isinstance(self.data, bytes):
            raise TypeError('Attribute \'data\' cannot be of type bytes-like object')
        data = str(self.data or '')
        # set content-length header if there is a message body
        if data:
            self.headers.content_length = len(data)
        return f'{str(self.headers)}{data}'

    def __bytes__(self, encoding='utf-8'):
        # if data is in bytes, we canot use self.__str__
        if isinstance(self.data, bytes):
            # set content-length header if there is a message body
            if self.data:
                self.headers.content_length = len(self.data)
            return bytes(str(self.headers), encoding) + self.data

        # can just render str and then convert to bytes
        return bytes(str(self), encoding)
