from pathlib import Path


class Settings:
    def __init__(self, verbosity: int = None, address: str = None, port: int = None, allowed_hosts: list = None,
                 allowed_methods: list = None, urls: dict = None, errors: dict = None,
                 cors: tuple = (None, None, None, None, None), static: tuple = (None, None), media: tuple = (None, None),
                 templates_dir=None, https: tuple = (None, None, None, None), mime: dict = None):
        # logging
        self.verbosity = verbosity

        # address and port
        self.address = (address, port)
        
        self.allowed_hosts = allowed_hosts
        self.allowed_methods = allowed_methods

        # cors
        self.cors_allowed_origins = cors[0]
        self.cors_allow_creds = cors[1]
        self.cors_allowed_headers = cors[2]
        self.cors_allowed_methods = cors[3]
        self.cors_max_age = cors[4]
        
        # views
        self.views = urls
        self.errors = errors or dict()
        
        # static
        self.static_url_base = static[0]
        self.static_files_dir = Path(static[1]) if static[1] else None
        
        # media
        self.media_url_base = media[0]
        self.media_files_dir = Path(media[1]) if media[1] else None
        
        # templates
        self.templates_dir = Path(templates_dir) if templates_dir else None

        # https
        self.use_https = https[0]
        self.https_cert_path = https[1]
        self.https_privkey_path = https[2]
        self.https_privkey_passwd = https[3]
        
        # mime
        self.supported_mimetypes = mime

    def override(self, local):
        check = lambda property_name, current_value: getattr(local, property_name, current_value)

        self.verbosity = check('VERBOSITY', self.verbosity)
        self.address = (local.ADDRESS, local.PORT)
        self.allowed_hosts = local.ALLOWED_HOSTS
        self.allowed_methods = check('ALLOWED_METHODS', self.allowed_hosts)
        self.views = local.urls
        self.errors = {**self.errors, **check( 'errors', dict())}

        # CORS
        self.cors_allowed_origins = check('CORS_ALLOWED_ORIGINS', self.cors_allowed_origins)
        self.cors_allow_creds = check('CORS_ALLOW_CREDENTIALS', self.cors_allow_creds)
        self.cors_allowed_headers = check('CORS_ALLOWED_HEADERS', self.cors_allowed_headers)
        self.cors_allowed_methods = check('CORS_ALLOWED_METHODS', self.cors_allowed_methods)
        self.cors_max_age = check('CORS_MAX_AGE', self.cors_max_age)

        # STATIC
        self.static_url_base = check('STATIC_URL_BASE', self.static_url_base)
        self.static_files_dir = check('STATIC_FILES_DIR', self.static_files_dir)
        self.static_files_dir = Path(self.static_files_dir) if self.static_files_dir else None

        # MEDIA
        self.media_url_base = check('MEDIA_URL_BASE', self.media_url_base)
        self.media_files_dir = check('MEDIA_FILES_DIR', self.media_files_dir)
        self.media_files_dir = Path(self.media_files_dir) if self.media_files_dir else None

        # TEMPLATING
        self.templates_dir = check('TEMPLATES_DIR', self.templates_dir)
        self.templates_dir = Path(self.templates_dir) if self.templates_dir else None

        # HTTPS
        self.use_https = check('USE_HTTPS', self.use_https)
        self.https_cert_path = check('CERTIFICATE_PATH', self.https_cert_path)
        self.https_cert_path = Path(self.https_cert_path) if self.https_cert_path else None
        self.https_privkey_path = check('PRIVATE_KEY_PATH', self.https_privkey_path)
        self.https_privkey_path = Path(self.https_privkey_path) if self.https_privkey_path else None
        self.https_privkey_passwd = check('PRIVATE_KEY_PASSWD', self.https_privkey_passwd)

        self.supported_mimetypes = check('SUPPORTED_MIMETYPES', self.supported_mimetypes)
