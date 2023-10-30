import pigeon.http.mime as mime
from pigeon.default.errors import fallback

SUPPORTED_MIMETYPES = {
    'application/json': mime.JSONParser,
    'application/x-www-form-urlencoded': mime.UrlencodedFormParser,
    'multipart/form-data': mime.MultiPartFormParser,
}

errors = {
    000: fallback,
}