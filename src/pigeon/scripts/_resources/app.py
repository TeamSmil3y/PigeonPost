import pigeon.core.server as server
from pigeon.conf.settings import Settings
import settings

def run():
    server.start(settings)
    

if __name__ == '__main__':
    run()
