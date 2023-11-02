import pigeon
from pigeon.utils.logger import create_log
import resources.settings as settings

log = create_log('TESTRUNNER', 'green')


def configure_environment():
    pigeon.conf.manager.override(settings)
    pigeon.conf.manager.setup()


def gather_tests():
    

def run():
    log(2, 'CONFIGURING ENVIRONMENT')
    configure_environment()
    
    log(2, 'RUNNING TESTS..')


if __name__ == '__main__':
    run()