"""
Constants and configurations for the pigeon middleware used when processing requests.
"""

from pigeon.middleware.processing import Owl, Raven
import pigeon.middleware.components as comp


# supported version of HTTP
HTTP_VERSIONS = ['1.1']

# request preprocessors
PROCESSORS = {
    '1.1': Owl,
    '2.0': Raven,
}

# preprocessing components
PREPROCESSING_COMPONENTS = [
    comp.host.HostComponent,
    comp.cors.CORSComponent,
    comp.method.MethodComponent,
    comp.connection.ConnectionComponent,
]
# postprocessing components
POSTPROCESSING_COMPONENTS = [
    comp.server.ServerComponent,
    comp.cors.CORSComponent,
    comp.connection.ConnectionComponent,
]
