from pigeon.conf import Manager
import pytest
from pathlib import Path
import pigeon.middleware.views as views
import pigeon.middleware.auth as auth
import tests.resources.settings as settings

TESTS_DIR = Path(__file__).parent.resolve()


@pytest.fixture(autouse=True, scope='module')
def restore():
    """
    Sets up and restores environment (settings, ...) before every test.
    """
    # override default settings with settings for test environment
    Manager.override(settings)

    # view handlers
    Manager.view_handler = views.ViewHandler()
    Manager.error_handler = views.ErrorHandler()
    # auth handlers
    Manager.auth_handler = auth.AuthHandler()

    # call manager.setup to configure runtime computed settings
    Manager._setup()
