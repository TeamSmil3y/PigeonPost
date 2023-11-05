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
        
        view_handler.register('/nottest/{{myparam}}/dynamic/', lambda request, dynamic: dynamic.myparam, '*/*')
        view_handler.register('/test/{{myparam}}/dynamic/', lambda request, dynamic: dynamic.myparam, '*/*')

    def test_dynamic_params_isolated(self):
        """
        Tests the get_func function of views.ViewHandler using dynamic params when the preceeding path before the param is not found in any other view.
        """
        view_handler: views.ViewHandler = settings.VIEWHANDLER

        func = view_handler.get_func('/nottest/thisisatest/dynamic/', '*/*')

        self.assertEqual(func(None), 'thisisatest', 'Gathering dynamic param from request failed!')

    def test_dynamic_params(self):
        """
        Tests the get_func function of views.ViewHandler using dynamic params when the preceeding path before is existent in an another view.
        """
        view_handler: views.ViewHandler = settings.VIEWHANDLER
        func = view_handler.get_func('/test/thisisatest/dynamic/', '*/*')

        self.assertEqual(func(None), 'thisisatest', 'Gathering dynamic param from request failed!')

    def test_get_available_mimetypes(self):
        """
        Tests the get_available_mimetypes function of views.ViewHandler used to retrieve a list of available mimetypes
        for a view in order of least specified (e.g. 'text/html') to most specified ('*/*').
        """
        view_handler: views.ViewHandler = settings.VIEWHANDLER
        available_views = view_handler.get_available_mimetypes('/test/')
        
        self.assertEqual(available_views, ['application/json', 'text/html', 'text/xml', 'image/gzip', 'text/*', '*/*'],
                         'Available mimetypes for view seem to be incorrect - content negotiation unreliable!')
