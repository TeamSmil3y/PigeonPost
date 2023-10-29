import protofire.http.mime as mime

SUPPORTED_MIMETYPES = {
    'application/json': mime.JSONParser,
    'application/x-www-form-urlencoded': mime.UrlencodedFormParser,
    'multipart/form-data': mime.MultiPartFormParser,
}