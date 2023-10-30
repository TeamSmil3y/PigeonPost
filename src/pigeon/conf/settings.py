from pathlib import Path
import pigeon.default.settings as default


class Settings:
    def __init__(self, address: str, port: int, urls: dict, errors: dict, cors: tuple,
                 static: tuple, media: tuple, templates_dir, https: tuple,
                 mime: dict):
        # address and port
        self.address = (address, port)
        
        # cors
        self.cors_allowed_origins = cors[0]
        self.cors_allow_creds = cors[1]
        
        # views
        self.views = urls
        self.errors = errors
        
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

    @classmethod
    def from_settings(cls, local):
        return Settings(
            address=local.ADDRESS,
            port=local.PORT,
            urls=local.urls,
            errors={**default.errors, **local.errors},
            cors=(local.CORS_ALLOWED_ORIGINS, local.CORS_ALLOW_CREDENTIALS),
            static=(
                getattr(local, 'STATIC_URL_BASE', None),
                getattr(local, 'STATIC_FILES_DIR', None),
            ),
            media=(
                getattr(local, 'MEDIA_URL_BASE', None),
                getattr(local, 'MEDIA_FILES_DIR', None),
            ),
            templates_dir=getattr(local, 'TEMPLATES_DIR', None),
            https=(
                getattr(local, 'USE_HTTPS', False),
                getattr(local, 'CERTIFICATE_PATH', ''),
                getattr(local, 'PRIVATE_KEY_PATH', ''),
                getattr(local, 'PRIVATE_KEY_PASSWD', ''),
            ),
            mime=(getattr(local, 'SUPPORTED_MIMETYPES', default.SUPPORTED_MIMETYPES)),
            )


settings_used = None


def use(settings: Settings):
    global settings_used
    settings_used = settings


def get():
    global settings_used
    return settings_used
