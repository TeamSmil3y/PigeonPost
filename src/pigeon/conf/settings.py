# VERBOSITY
VERBOSITY = 2

# ADDRESS
ADDRESS = ''
PORT = 8080

# ALLOWED HOSTS
ALLOWED_HOSTS = ['*']
# ALLOWED METHODS
ALLOWED_METHODS = ['POST', 'GET', 'HEAD', 'POST', 'PUT', 'OPTIONS']

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

# EXCEPTION HANDLING & DEBUG MODE
CRASH_ON_FAILURE = False
DEBUG_MODE = True

# MIME PARSERS
MIME_PARSERS = {
    'application/json': 'pigeon.middleware.conversion.mime.parsers.JSONParser',
    'application/x-www-form-urlencoded': 'pigeon.middleware.conversion.mime.parsers.UrlencodedFormParser',
    'multipart/form-data': 'pigeon.middleware.conversion.mime.parsers.MultiPartFormParser',
}

# MIME GENERATORS
MIME_GENERATORS = {
    'application/json': 'pigeon.middleware.conversion.mime.generators.JSONGenerator',
}
