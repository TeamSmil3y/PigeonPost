import protofire.core.server as server
from protofire.core.settings import Settings
import settings as local


def run():
    server.start(
        Settings(
            address=local.ADDRESS,
            port=local.PORT,
            urls=local.urls,
            errors=local.errors,
            cors=(local.CORS_ALLOWED_ORIGINS, local.CORS_ALLOW_CREDENTIALS),
            static=(local.STATIC_URL_BASE, local.STATIC_FILES_DIR),
            media=(local.MEDIA_URL_BASE, local.MEDIA_FILES_DIR),
            https=(local.USE_HTTPS, local.CERTIFICATE_PATH, local.PRIVATE_KEY_PATH, local.PRIVATE_KEY_PASSWD)
        )
    )
    

if __name__ == '__main__':
    run()
