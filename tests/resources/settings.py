import pathlib
import pigeon.http.parsing.mime
import pigeon.default.errors

BASE_DIR = pathlib.Path(__file__).parent.resolve()

# VERBOSITY
VERBOSITY = 4

# ADDRESS
ADDRESS = ''
PORT = 8080

# ALLOWED HOSTS
ALLOWED_HOSTS = ['example.org']
# ALLOWED METHODS
ALLOWED_METHODS = ['POST', 'GET', 'HEAD', 'POST', 'PUT', 'OPTIONS']

# ERRORS (VIEWS BUT FOR ERRORS)
ERRORS = {
    000: pigeon.default.errors.fallback,
}

# ACCESS-CONTROL
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_CRED = False
CORS_ALLOWED_HEADERS = ['Content-Type']
CORS_ALLOWED_METHODS = ['POST', 'GET', 'HEAD', 'POST', 'PUT', 'OPTIONS']
CORS_MAX_AGE = 1200

# STATICFILES
STATIC_URL_BASE = None
STATIC_FILES_DIR = None

# MEDIAFILES
MEDIA_URL_BASE = None
MEDIA_FILES_DIR = None

# TEMPLATING
TEMPLATES_DIR = None

# HTTPS
USE_HTTPS = False
CERTIFICATE_PATH = None
PRIVATE_KEY_PATH = None
PRIVATE_KEY_PASSWD = None

# MIME
SUPPORTED_MIMETYPES = {
    'application/json': pigeon.http.parsing.mime.JSONParser,
    'application/x-www-form-urlencoded': pigeon.http.parsing.mime.UrlencodedFormParser,
    'multipart/form-data': pigeon.http.parsing.mime.MultiPartFormParser,
}

MIDDLEWARE = None
