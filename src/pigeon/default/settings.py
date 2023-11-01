import pigeon.http.parsing.mime as mime
from pigeon.default.errors import fallback

# LOGGING
VERBOSITY = 2

# ADDRESS and PORT
ADDRESS = ''
PORT = 8080

# ALLOWED HOSTS
ALLOWED_HOSTS = None

# ALLOWED METHODS
ALLOWED_METHODS = ['POST', 'GET', 'HEAD', 'POST', 'PUT', 'OPTIONS']

# VIEWS
urls = {

}
# ERROS
errors = {
    000: fallback,
}

# CORS
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOWED_HEADERS = ['Content-Type']
CORS_ALLOWED_METHODS = ['POST', 'GET', 'HEAD', 'POST', 'PUT', 'OPTIONS']
CORS_MAX_AGE = 1200

# STATIC
STATIC_URL_BASE = None
STATIC_FILES_DIR = None

# MEDIA
MEDIA_URL_BASE = None
MEDIA_FILES_DIR = None

# TEMPLATES
TEMPLATES_DIR = None

# HTTPS
USE_HTTPS = False
CERTIFICATE_PATH = None
PRIVATE_KEY_PATH = None
PRIVATE_KEY_PASSWD = None

# MIME
SUPPORTED_MIMETYPES = {
    'application/json': mime.JSONParser,
    'application/x-www-form-urlencoded': mime.UrlencodedFormParser,
    'multipart/form-data': mime.MultiPartFormParser,
}
