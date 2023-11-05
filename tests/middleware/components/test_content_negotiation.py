import pytest
from pigeon.http import HTTPRequest
from pigeon.conf import Manager
from pigeon.middleware.components.content_negotiation import ContentNegotiationComponent
from tests import restore


def test_parse_accept_versioned():
    """
    Tests the parse_accept_header function with version params in the 'Accept' header
    """
    dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Accept': 'text/html,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'})
    parsed = ContentNegotiationComponent.parse_accept_header(dummy_request)
    assert parsed == ('text/html', '*/*', 'application/signed-exchange')

def test_header_parser():
    """
    Tests the ContentNegotiationComponent.parse_accept_header function used to parse Content-Negotiation headers
    """
    # create dummy headers for parser
    dummy_headers: tuple[str, ...] = ('text/plain,application/json;q=0.5, text/*;q=0.6',
                                      'gzip, deflate;q=0.8,br;q=0.9',
                                      'en;q=0.3,de, ca;q=0.6')
    # parse dummy headers
    parsed = []
    for dummy_header in dummy_headers:
        parsed.append(ContentNegotiationComponent.parse_header(dummy_header))

    assert parsed[0] == ('text/plain', 'text/*', 'application/json')
    assert parsed[1] == ('gzip', 'br', 'deflate')
    assert parsed[2] == ('de', 'ca', 'en')


def test_parse_accept_header():
    """
    Tests the ContentNegotiationComponent.parse_accept_header function used to parse the 'Accept' header
    """
    # create dummy request and parse Accept header
    dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Accept': 'text/plain,application/json;q=0.5, text/*;q=0.6'})
    parsed = ContentNegotiationComponent.parse_accept_header(dummy_request)
    assert parsed == ('text/plain', 'text/*', 'application/json')


def test_parse_accept_encoding_header():
    """
    Tests the ContentNegotiationComponent.parse_accept_encoding_header function used to parse the 'Accept-Encoding' header
    """
    # create dummy request and parse Accept header
    dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Accept-Encoding': 'gzip, deflate;q=0.8,br;q=0.9'})
    parsed = ContentNegotiationComponent.parse_accept_encoding_header(dummy_request)
    assert parsed == ('gzip', 'br', 'deflate')


@pytest.mark.skip(reason='parse language not implemented - skipping test')
def test_parse_accept_language_header():
    """
    Tests the ContentNegotiationComponent.parse_accept_language_header function used to parse the 'Accept-Language' header
    """
    # create dummy request and parse Accept header
    dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Accept-Language': 'en;q=0.3,de, ca;q=0.6'})
    parsed = ContentNegotiationComponent.parse_accept_language_header(dummy_request)
    assert parsed == ('de', 'ca', 'en')
