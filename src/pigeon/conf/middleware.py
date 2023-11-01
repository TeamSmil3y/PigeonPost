"""
Constants and configurations for the pigeon middleware used when processing requests.
"""

from pigeon.middleware.processing import Owl, Raven
import pigeon.middleware.components as comp


# SUPPORTED VERION OF HTTP
HTTP_VERSIONS = ['1.1']

# REQUEST PREPROCESSOR
PROCESSORS = {
    '1.1': Owl,
    '2.0': Raven,
}

# PREPROCESSING COMPONENTS (COMPONENTS USED BY PREPROCESSOR)
PREPROCESSING_COMPONENTS = [
    comp.host.HostComponent,
    comp.cors.CORSComponent,
    comp.method.MethodComponent,
    comp.connection.ConnectionComponent,
    comp.connection.CacheControlComponent,
]
# POSTPROCESSING COMPONENTS (COMPONENTS USED BY POSTPROCESSOR)
POSTPROCESSING_COMPONENTS = [
    comp.server.ServerComponent,
    comp.cors.CORSComponent,
    comp.connection.ConnectionComponent,
    comp.connection.CacheControlComponent,
]

#