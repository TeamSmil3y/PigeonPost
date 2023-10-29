import protofire.core.settings as _settings
from protofire.http.http import HttpRequest, HttpResponse
from protofire.http.errors import error
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


def handle_media_request(request: HttpRequest):
    settings = _settings.get()
    local_path = settings.media_files_dir / Path(request.path[len(settings.media_url_base):])

    if not local_path.resolve().is_relative_to(settings.media_files_dir):
        # attempting to access resource outside of static_files_dir (directory traversal)
        return error(404, request)

    if os.path.exists(local_path):
        # return file
        data, encoding = fetch_file(local_path,
                                    [encoding.strip() for encoding in request.headers('Accept-Encoding').split(',')])

        # get mimetype for file
        mimetype = mimetypes.guess_type(local_path)[0]

        # make response with file
        with open(local_path, 'r') as f:
            response = HttpResponse(data=data)
            response.set_headers({'Content-Type': mimetype})
            if encoding:
                response.set_headers({'Content-Encoding': encoding})
            return response
    else:
        return error(404, request)
