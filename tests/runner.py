import pigeon
import pigeon.utils.logger as logger
import imp
from pathlib import Path
import sys
import unittest

TESTS_DIR = Path(__file__).parent.resolve()
sys.path.append(TESTS_DIR)
settings = imp.load_source('settings', str(TESTS_DIR) + '/resources/settings.py')

log = logger.Log('TESTRUNNER', '#aaffaa')

def restore_environment():
    # override default settings with settings for test environment
    pigeon.conf.manager.override(settings)
    # call manager.setup to configure runtime computed settings
    pigeon.conf.manager.setup()

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(TESTS_DIR)
    runner = unittest.TextTestRunner()
    runner.run(suite)


def main():
    log.info('CONFIGURING ENVIRONMENT')
    restore_environment()
    
    log.info('RUNNING TESTS..')
    run_tests()


if __name__ == '__main__':
    main()
