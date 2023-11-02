from pigeon.files import handle_media_request
from typing import Callable
from pigeon.http import HTTPRequest, HTTPResponse
from pigeon.conf import settings


class MediaFilesComponent:
    @classmethod
    def process(cls, request: HTTPRequest, callback: Callable) -> (HTTPRequest, Callable):
        """
        If request is to a media url change callback to return media file, otherwise leave as is.
        """
        if settings.MEDIA_URL_BASE and request.path.startswith(settings.MEDIA_URL_BASE):
            # request for static file
            request.tags.is_media_request = True
            return request, handle_media_request
        return request, callback