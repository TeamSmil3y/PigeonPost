import pigeon.conf.manager
import pytest
from pathlib import Path
import tests.resources.settings as settings

TESTS_DIR = Path(__file__).parent.resolve()


@pytest.fixture(autouse=True, scope='module')
def restore():
    """
    Sets up and restores environment (settings, ...) before every test.
    """
    # override default settings with settings for test environment
    pigeon.conf.manager.override(settings)
    # call manager.setup to configure runtime computed settings
    pigeon.conf.manager.setup()