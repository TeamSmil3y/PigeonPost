import pigeon.conf.manager
import imp
import pytest
import pigeon.utils.logger as logger
import sys
from pathlib import Path

log = logger.Log('TESTS', '#aaffaa')
TESTS_DIR = Path(__file__).parent.resolve()
sys.path.append(TESTS_DIR)
settings = imp.load_source('settings', str(TESTS_DIR) + '/resources/settings.py')

@pytest.fixture(autouse=True)
def setup_test():
    """
    Sets up and restores environment (settings, ...) before every test.
    """
    log.log(f'RESTORING ENVIRONMENT', color='yellow')
    print(43532452342342)
    # override default settings with settings for test environment
    pigeon.conf.manager.override(settings)
    # call manager.setup to configure runtime computed settings
    pigeon.conf.manager.setup()