from pigeon.files import handle_static_request
from typing import Callable
from pigeon.http import HTTPRequest, HTTPResponse
from pigeon.conf import settings


class StaticFilesComponent:
    @classmethod
    def process(cls, request: HTTPRequest, callback: Callable) -> (HTTPRequest, Callable):
        """
        If request is to a static url change callback to return static file, otherwise leave as is.
        """

        if settings.STATIC_URL_BASE and request.path.startswith(settings.STATIC_URL_BASE):
            # request for static file
            request.tags.is_static_request = True
            return request, handle_static_request
        return request, callback