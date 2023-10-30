import pigeon.core.server as server
from pigeon.conf.settings import Settings
import settings as local

def run():
    server.start(
        Settings.from_settings(local)
    )
    

if __name__ == '__main__':
    run()
