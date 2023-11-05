from pigeon.files import handle_media_request
from typing import Callable
from pigeon.http import HTTPRequest, HTTPResponse
from pigeon.conf import Manager


class MediaFilesComponent:
    @classmethod
    def process(cls, request: HTTPRequest, func: Callable) -> (HTTPRequest, Callable):
        """
        If request is to a media url change func to return media file, otherwise leave as is.
        """
        if Manager.media_url_base and request.path.startswith(Manager.media_url_base):
            # request for static file
            request.tags.is_media_request = True
            return request, handle_media_request
        return request, func
