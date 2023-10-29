from pathlib import Path

class Settings:
    def __init__(self, address: str, port: int, urls: dict, errors: dict, cors: tuple = ([''], False),
                 static: tuple = (None, None), media: tuple = (None, None), https: tuple = (False, '', '', '')):
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

        # https
        self.use_https = https[0]
        self.https_cert_path = https[1]
        self.https_privkey_path = https[2]
        self.https_privkey_passwd = https[3]


settings_used = None


def use(settings: Settings):
    global settings_used
    settings_used = settings


def get():
    global settings_used
    return settings_used
