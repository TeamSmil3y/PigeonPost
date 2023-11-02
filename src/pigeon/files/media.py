from pigeon.conf import settings
from pigeon.http import HTTPRequest, HTTPResponse
from pigeon.http.common import error, status
from pathlib import Path
import mimetypes
import gzip
import os


def fetch_file(local_path: Path, encodings):
    """
    Returns file at the requested path using possible encoding
    """
    # file is not loaded into memory
    with open(local_path, 'rb') as f:
        data = f.read()
    
    if 'gzip' in encodings:
        return gzip.compress(data), 'gzip'
    else:
        return data, None


def handle_media_request(request: HTTPRequest):
    local_path = settings.MEDIA_FILES_DIR / Path(request.path[len(settings.MEDIA_URL_BASE):])

    if not local_path.resolve().is_relative_to(settings.MEDIA_FILES_DIR):
        # attempting to access resource outside of static_files_dir (directory traversal)
        return error(404, request)

    if os.path.exists(local_path) and os.path.isfile(local_path):
        # return file
        data, encoding = fetch_file(local_path, request.accept_encodings)

        # get mimetype for file
        mimetype = mimetypes.guess_type(local_path)[0]

        # make response with file
        with open(local_path, 'r') as f:
            response = HTTPResponse(data=data)
            response.set_headers({'Content-Type': mimetype})
            if encoding:
                response.set_headers({'Content-Encoding': encoding})
        return response
    else:
        return error(404, request)
