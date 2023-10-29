import protofire.core.server as server
import protofire.conf.settings as settings
import settings as local


def run():
    server.start(
        settings.from_settings(local)
    )
    

if __name__ == '__main__':
    run()
