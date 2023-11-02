from pigeon.http import HTTPRequest, HTTPResponse, error
from typing import Callable
import pigeon.middleware.components as comp
from pigeon.conf import settings
from pigeon.utils.logger import create_log


class Processor:
    @classmethod
    def preprocess(cls,  request: HTTPRequest) -> HTTPRequest | HTTPResponse:
        raise NotImplementedError

    @classmethod
    def process(cls, request: HTTPRequest, callback: Callable) -> (HTTPRequest, Callable):
        raise NotImplementedError

    @classmethod
    def postprocess(cls,  response: HTTPResponse,  request: HTTPRequest) -> HTTPResponse:
        raise NotImplementedError


class ComponentProcessor(Processor):
    preprocessing_components = []
    processing_components = []
    postprocessing_components = []

    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.log = create_log('MIDDLEWARE', 'green', subname=cls.__name__)
        super().__init_subclass__(**kwargs)

    @classmethod
    def preprocess(cls, request: HTTPRequest) -> HTTPRequest | HTTPResponse:
        # run every middleware preprocess comnponent on request
        for component in cls.preprocessing_components:
            cls.log(4, f'PREPROCESSING WITH COMPONENT: {component.__name__}')
            request = component.preprocess(request=request)
            # request is an error response and should not be processed further
            if request.is_error:
                return request
        return request

    @classmethod
    def process(cls, request: HTTPRequest) -> HTTPResponse:
        # gather response for request
        callback = lambda request: error(404)

        # run every middleware process component on request and callback
        for component in cls.processing_components:
            cls.log(4, f'PROCESSING WITH COMPONENT: {component.__name__}')
            request, callback = component.process(request=request, callback=callback)

        return callback(request)

    @classmethod
    def postprocess(cls,  response: HTTPResponse,  request: HTTPRequest) -> HTTPResponse:
        # run every middleware postprocess component on response
        for component in cls.postprocessing_components:
            cls.log(4, f'PREPROCESSING WITH COMPONENT: {component.__name__}')
            response = component.postprocess(response=response, request=request)
            if response.is_error:
                return response
        return response


class Owl(ComponentProcessor):
    """
    Processes requests using the HTTP/1.1 protocol
    """
    preprocessing_components = [
        comp.host.HostComponent,
        comp.cors.CORSComponent,
        comp.method.MethodComponent,
        comp.connection.ConnectionComponent,
        comp.cache_control.CacheControlComponent,
        comp.content_negotiation.ContentNegotiationComponent,
    ]
    processing_components = [
        comp.content_negotiation.ContentNegotiationComponent,
        comp.staticfiles.StaticFilesComponent,
        comp.mediafiles.MediaFilesComponent,
    ]
    postprocessing_components = [
        comp.server.ServerComponent,
        comp.cors.CORSComponent,
        comp.connection.ConnectionComponent,
        comp.cache_control.CacheControlComponent,
        comp.content_negotiation.ContentNegotiationComponent,
    ]


class Raven(ComponentProcessor):
    """
    Processes requests using the HTTP/2.0 protocol
    """
    pass
