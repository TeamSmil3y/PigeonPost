from pigeon.http import HTTPRequest
from pigeon.middleware.components.host import HostComponent
from tests import restore

def test_allowed_host(restore):
    """
    Tests the HostComponent.allowed_host function used to check whether the Host header in a request is valid
    """
    # test with a valid host header
    dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Host': 'example.org'})
    is_allowed = HostComponent.allowed_host(dummy_request)
    assert is_allowed

    # test with invalid host header
    dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Host': 'wrong_host.invalid'})
    is_allowed = HostComponent.allowed_host(dummy_request)
    assert not is_allowed
