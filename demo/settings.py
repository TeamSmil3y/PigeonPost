import pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()

# LOGGIN VERBOSITY
VERBOSITY = 4

# ADDRESS AND PORT
ADDRESS = ''
PORT = 8080

# ACCESS-CONTROL
ALLOWED_HOSTS = ['*']
CORS_ALLOWED_ORIGINS = [
    'http://localhost',
    'https://localhost',
    'http://localhost:3001'
]
CORS_ALLOW_CREDENTIALS = False

# STATIC FILES
STATIC_URL_BASE = '/static/'
STATIC_FILES_DIR = BASE_DIR / 'static/'

# MEDIA FILES
MEDIA_URL_BASE = '/media/'
MEDIA_FILES_DIR = BASE_DIR / 'media/'

# TEMPLATES
TEMPLATES_DIR = BASE_DIR / 'templates/'

# HTTPS
USE_HTTPS = False
CERTIFICATE_PATH = ''
PRIVATE_KEY_PATH = ''
PRIVATE_KEY_PASSWD = ''
