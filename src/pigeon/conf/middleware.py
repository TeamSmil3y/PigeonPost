"""
Constants and configurations for the pigeon middleware used when processing requests.
"""

from pigeon.middleware.processing import Owl, Raven


# SUPPORTED VERION OF HTTP
HTTP_VERSIONS = ['1.1']

# REQUEST PREPROCESSOR
PROCESSORS = {
    '1.1': Owl,
    '2.0': Raven,
}
