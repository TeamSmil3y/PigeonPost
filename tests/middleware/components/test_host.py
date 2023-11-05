from pigeon.http import HTTPRequest
from pigeon.middleware.components.host import HostComponent


def test_allowed_host(self):
    """
    Tests the HostComponent.allowed_host function used to check whether the Host header in a request is valid
    """
    # test with a valid host header
    dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Host': 'example.org'})
    is_allowed = HostComponent.allowed_host(dummy_request)
    self.assertEqual(True, is_allowed, 'Host header was wrongfuly identified as disallowed')

    # test with invalid host header
    dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Host': 'wrong_host.invalid'})
    is_allowed = HostComponent.allowed_host(dummy_request)
    self.assertEqual(False, is_allowed, 'Host header was wrongfuly identified as allowed')
