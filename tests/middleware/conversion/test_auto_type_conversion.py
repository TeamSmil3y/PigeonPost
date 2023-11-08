import pigeon.middleware.conversion.converter as converter
import pigeon.middleware.conversion.mime.generators as generators
from tests.setup_test import restore


def test_automatic_type_conversion(restore):
    """
    Tests the converter.generate function used to generate valid HTTPResponses from
    """
    data = {'This is': 'a test', 'and it': 'hopfefully succeeds'}
    response = converter.generate(data, 'application/json')

    assert response.data == '{"This is": "a test", "and it": "hopfefully succeeds"}'
