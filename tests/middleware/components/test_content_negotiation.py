import pytest
from pigeon.http import HTTPRequest
from pigeon.conf import Manager
from pigeon.middleware.components.content_negotiation import ContentNegotiationComponent
from tests import restore

@pytest.mark.skip(reason='broken test - skipping')
def test_find_func():
    """
    Tests the ContentNegotiationComponent.find_func function used to find views for a list of possible Content-Types
    """
    # Define a sample list of Content-Types and Accept headers
    test_content_types = [('text/html;q=0.3, application/json, text/xml;q=0.5', 'application/json'),
                          ('text/html;q=0.9, application/json;q=0.3, text/xml;q=0.5', 'text/html'),
                          ('text/*;q=0.5,text/xml', 'text/html'),
                          ('text/*;q=0.9, image/gzip', 'image/*'),
                          ('text/html;q=0.3, text/xml;q=0.4, application/x-www-urlencoded', 'text/xml'),
                          ('text/xml, application/x-www-urlencoded', '*/*')]

    # Test finding func for each content type
    for accept_header, content_type in test_content_types:
        request = HTTPRequest('GET', '/', headers={'Accept': accept_header})
        request = ContentNegotiationComponent.preprocess(request)

        assert isinstance(request, HTTPRequest)

        func = ContentNegotiationComponent.find_func(request)
        assert not isinstance(func, None)

        # Ensure the returned response
        response = func(request)

        # Ensure the response data matches the expected Content-Type
        assert content_type == response


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
