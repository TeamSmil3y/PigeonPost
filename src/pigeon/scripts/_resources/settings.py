import pathlib
BASE_DIR = pathlib.Path(__file__).parent.resolve()

# ADDRESS AND PORT
ADDRESS = ''
PORT = 80

# VIEWS
urls = {
}
errors = {
}

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost',
    'https://localhost',
]
CORS_ALLOW_CREDENTIALS = False
