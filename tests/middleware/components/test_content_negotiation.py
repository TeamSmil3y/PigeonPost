import testcases
from pigeon.http import HTTPRequest
import pigeon.conf.settings as settings
from pigeon.middleware.components.content_negotiation import ContentNegotiationComponent


class TestContentNegotiationComponent(testcases.BaseTestCase):

    @classmethod
    def set_up_class(cls):
        # add dummy typed views
        settings.TYPED_VIEWS = {
            '/': {
                'application/json': lambda request: 'application/json',
                'text/html': lambda request: 'text/html',
                'text/plain': lambda request: 'text/plain',
                'image/*': lambda request: 'image/*',
                'application/*': lambda request: 'application/*',
                '*/*': lambda request: '*/*',
                }
        }

    def unused_test_find_callback(self):
        """
        Tests the ContentNegotiationComponent.find_callback function used to find views for a list of possible Content-Types
        """
        # Define a sample list of Content-Types and Accept headers
        test_content_types = [('text/html;q=0.3, application/json, text/xml;q=0.5', 'application/json'),
                              ('text/html;q=0.9, application/json;q=0.3, text/xml;q=0.5', 'text/html'),
                              ('text/*;q=0.5,text/xml', 'text/html'),
                              ('text/*;q=0.9, image/gzip', 'image/*'),
                              ('text/html;q=0.3, text/xml;q=0.4, application/x-www-urlencoded', 'text/xml'),
                              ('text/xml, application/x-www-urlencoded', '*/*')]

        # Test finding callback for each content type
        for accept_header, content_type in test_content_types:
            request = HTTPRequest('GET', '/', headers={'Accept': accept_header})
            request = ContentNegotiationComponent.preprocess(request)
            
            self.assertIsInstance(request, HTTPRequest, f"ContentNegotiationComponent.preprocess returned an HTTPResponse - possible error")
            
            callback = ContentNegotiationComponent.find_callback(request)
            self.assertIsNotNone(callback, f"Callback not found for Content-Type: {content_type}")

            # Ensure the returned response
            response = callback(request)

            # Ensure the response data matches the expected Content-Type
            self.assertEqual(content_type, response, f"Response data does not match expected Content-Type: {content_type}")
    
    def test_header_parser(self):
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

        msg = 'ContentNegotiationComponent failed parsing Content-Negotiation headers'
        self.assertEqual(parsed[0], ('text/plain', 'text/*', 'application/json'), msg)
        self.assertEqual(parsed[1], ('gzip', 'br', 'deflate'), msg)
        self.assertEqual(parsed[2], ('de', 'ca', 'en'), msg)

    def test_parse_accept_header(self):
        """
        Tests the ContentNegotiationComponent.parse_accept_header function used to parse the 'Accept' header
        """
        # create dummy request and parse Accept header
        dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Accept': 'text/plain,application/json;q=0.5, text/*;q=0.6'})
        parsed = ContentNegotiationComponent.parse_accept_header(dummy_request)
        self.assertEqual(parsed, ('text/plain', 'text/*', 'application/json'), 'ContentNegotiationComponent failed parsing Accept Header')

    def test_parse_accept_encoding_header(self):
        """
        Tests the ContentNegotiationComponent.parse_accept_encoding_header function used to parse the 'Accept-Encoding' header
        """
        # create dummy request and parse Accept header
        dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Accept-Encoding': 'gzip, deflate;q=0.8,br;q=0.9'})
        parsed = ContentNegotiationComponent.parse_accept_encoding_header(dummy_request)
        self.assertEqual(parsed, ('gzip', 'br', 'deflate'), 'ContentNegotiationComponent failed parsing Accept-Encoding Header')

    def unused_test_parse_accept_language_header(self):
        """
        Tests the ContentNegotiationComponent.parse_accept_language_header function used to parse the 'Accept-Language' header
        """
        # create dummy request and parse Accept header
        dummy_request: HTTPRequest = HTTPRequest('GET', '/', {'Accept-Language': 'en;q=0.3,de, ca;q=0.6'})
        parsed = ContentNegotiationComponent.parse_accept_language_header(dummy_request)
        self.assertEqual(parsed, ('de', 'ca', 'en'), 'ContentNegotiationComponent failed parsing Accept-Language Header')
