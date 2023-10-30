import pigeon.conf.settings as _settings
from pigeon.http import HTTPRequest, HTTPResponse
from pigeon.http.common import error
from pathlib import Path
import mimetypes
import gzip
import os

loaded_files = dict()


def load():
    """
    loads smaller static files into memory
    """
    settings = _settings.get()
    directory_base = settings.static_files_dir

    for directory, sub_directories, files in os.walk(directory_base):
        for file in files:
            local_path = Path(directory) / Path(file)
            compressed = load_file(local_path)
            # if nothing is returned file is too large
            if compressed:
                loaded_files[local_path] = compressed
    
def load_file(local_path: Path):
    """
    Tries loading a file into memory and compress it.
    If the file is too large, nothing will be returned.
    """
    # files over size of 5MB will not be loaded
    if os.path.getsize(local_path) < 5*10**5:
        with open(local_path,  'rb') as f:
            data = f.read()
            gzip_compressed = gzip.compress(data)
        return {None: data, 'gzip': gzip_compressed}
    return None


def fetch_file(local_path: Path, encodings):
    """
    Returns file at the requested path using possible encoding
    """
    global loaded_files
    if local_path in loaded_files:
        # file is loaded into memory, use encoding if possible
        encoding = 'gzip' if ('gzip' in encodings) else None
        return loaded_files[local_path][encoding], encoding
    else:
        # file is not loaded into memory
        with open(local_path, 'rb') as f:
            data = f.read()
        
        if 'gzip' in encodings:
            return gzip.compress(data), 'gzip'
        else:
            return data, None


def handle_static_request(request: HTTPRequest):
    settings = _settings.get()
    local_path: Path = settings.static_files_dir / Path(request.path[len(settings.static_url_base):])
    
    if not local_path.resolve().is_relative_to(settings.static_files_dir):
        # attempting to access resource outside of static_files_dir (directory traversal)
        return error(404, request)
    
    if os.path.exists(local_path) and os.path.isfile(local_path):
        # return file
        data, encoding = fetch_file(local_path, [encoding.strip() for encoding in request.headers('Accept-Encoding').split(',')])
        
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
