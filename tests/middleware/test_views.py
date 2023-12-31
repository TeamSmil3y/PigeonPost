import pytest
from pigeon.conf import Manager
import pigeon.middleware.views as views
from tests.setup_test import restore


@pytest.fixture(autouse=True, scope='module')
def set_up(restore):
    # define some dummy views
    view_handler: views.ViewHandler = views.ViewHandler()
    Manager.view_handler = view_handler

    view_handler.register('/test/', lambda request: 'application/json', 'application/json', None)
    view_handler.register('/test/', lambda request: 'text/html', 'text/html', None)
    view_handler.register('/test/', lambda request: '*/*', '*/*', None)
    view_handler.register('/test/', lambda request: 'text/xml', 'text/xml', None)
    view_handler.register('/test/', lambda request: 'text/*', 'text/*', None)
    view_handler.register('/test/', lambda request: 'image/gzip', 'image/gzip', None)

    view_handler.register('/nottest/{{myparam}}/dynamic/', lambda request, dynamic_params: dynamic_params.myparam, '*/*', None)
    view_handler.register('/test/{{myparam}}/dynamic/', lambda request, dynamic_params: dynamic_params.myparam, '*/*', None)


def test_dynamic_params_isolated():
    """
    Tests the get_func function of views.ViewHandler using dynamic params when the preceeding path before the param is not found in any other view.
    """
    view_handler: views.ViewHandler = Manager.view_handler

    func = view_handler.get_func('/nottest/thisisatest/dynamic/', '*/*')

    assert func(None).data == 'thisisatest', 'Gathering dynamic param from request failed!'


def test_dynamic_params():
    """
    Tests the get_func function of views.ViewHandler using dynamic params when the preceeding path before is existent in an another view.
    """
    view_handler: views.ViewHandler = Manager.view_handler
    func = view_handler.get_func('/test/thisisatest/dynamic/', '*/*')

    assert func(None).data == 'thisisatest', 'Gathering dynamic param from request failed!'


def test_get_available_mimetypes():
    """
    Tests the get_available_mimetypes function of views.ViewHandler used to retrieve a list of available mimetypes
    for a view in order of least specified (e.g. 'text/html') to most specified ('*/*').
    """
    view_handler: views.ViewHandler = Manager.view_handler
    available_views = view_handler.get_available_mimetypes('/test/')

    assert available_views == ['application/json', 'text/html', 'text/xml', 'image/gzip', 'text/*', '*/*']
