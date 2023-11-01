import pigeon.core.server as server
import settings as settings

def run():
    server.start(
        settings_used=settings
    )
    

if __name__ == '__main__':
    run()
