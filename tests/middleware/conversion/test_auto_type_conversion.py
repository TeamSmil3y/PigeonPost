import testcases
from pigeon.http import HTTPRequest
import pigeon.middleware.conversion.converter as converter
import pigeon.middleware.conversion.mime.generators as generators


class TestAutomaticTypeConversion(testcases.BaseTestCase):
    def test_automatic_type_conversion(self):
        """
        Tests the converter.generate function used to generate valid HTTPResponses from 
        """
        data = {'This is': 'a test', 'and it': 'hopfefully succeeds'}
        response = converter.generate(data, 'application/json')
        
        self.assertEqual(response.DATA, '{"This is": "a test", "and it": "hopfefully succeeds"}', 'Generating response from JSON str response body failed!')
        
    def test_json_generator(self):
        """
        Tests the generators.JSONGenerator.generate function used to generate a string from JSON data
        """
        data = {'This is': 'a test', 'and it': 'hopfefully succeeds'}
        generated = generators.JSONGenerator.generate(data=data)
        
        self.assertEqual(generated, '{"This is": "a test", "and it": "hopfefully succeeds"}', 'Generating string from JSON data failed!')