import testcases
from pigeon.http import HTTPRequest
import pigeon.conf.settings as settings
import pigeon.middleware.views as views


class TestViews(testcases.BaseTestCase):
    @classmethod
    def set_up_class(cls):
        # define some dummy views
        view_handler: views.ViewHandler = views.ViewHandler()
        settings.VIEWHANDLER = view_handler
        
        view_handler.register('/test/', lambda request: 'application/json', 'application/json')
        view_handler.register('/test/', lambda request: 'text/html', 'text/html')
        view_handler.register('/test/', lambda request: '*/*', '*/*')
        view_handler.register('/test/', lambda request: 'text/xml', 'text/xml')
        view_handler.register('/test/', lambda request: 'text/*', 'text/*')
        view_handler.register('/test/', lambda request: 'image/gzip', 'image/gzip')
        
    def test_dynamic_params(self):
        """
        Tests  ...
        """
        pass
        
    def test_get_available_mimetypes(self):
        """
        Tests the get_available_mimetypes function of views.ViewHandler used to retrieve a list of available mimetypes
        for a view in order of least specified (e.g. 'text/html') to most specified ('*/*').
        """
        view_handler: views.ViewHandler = settings.VIEWHANDLER
        available_views = view_handler.get_available_mimetypes('/test/')
        
        self.assertEqual(available_views, ['application/json', 'text/html', 'text/xml', 'image/gzip', 'text/*', '*/*'],
                         'Available mimetypes for view seem to be incorrect - content negotiation unreliable!')