import pigeon
from pigeon.utils.logger import create_log
import resources.settings as settings
from pathlib import Path
import os
import importlib.util
import unittest

TESTS_DIR = Path(__file__).parent.resolve()

log = create_log('TESTRUNNER', 'green')


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
    log(2, 'CONFIGURING ENVIRONMENT')
    restore_environment()
    
    log(2, 'RUNNING TESTS..')
    run_tests()


if __name__ == '__main__':
    main()
