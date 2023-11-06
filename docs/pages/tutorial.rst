Tutorial
========

Views
-----
Pigeon supports both untyped views and typed views.
Views that do not specify a mimetype default to being untyped.
Untyped views should always return either HTTPResponse objects or strings.::

    from pigeon import Pigeon
    app = Pigeon()

    @app.view('/')
    def home(request):
        return '<h1>Hello World!</h1>'

    @app.view('/welcome')
    def welcome(request):
        return HTTPResponse(data='Welcome!')

We can also add *typed views* by passing the mimetype of our view as the second argument for `app.view`.
Pigeon will automatically choose the most fitting typed view for the requested path depending on the `Accept` header::

    from pigeon.shortcuts import HTTPResponse, JSONResponse
    import json

    @app.view('/api/test', 'application/json')
    def api_test(request):
        return HTTPResponse(data=json.dumps({'Hello':'World!'}))

    @app.view('/api/test', 'text/plain')
    def api_test(request):
        return HTTPResponse(data='Hello World!')

In contrast to normal views, typed views supports automatic conversion of return data to HTTPResponse objects.
This means that a view with the mimetype `application/json` can return any JSON convertible data such as dicts, list, ...::

    @app.view('/api/test', 'application/json')
    def api_test(request):
        return {'this data is':'autoconverted to an HTTPResponse object'}

If we want to process data provided in the request, we can use the `get`, `data`, and `files` functions::

    @app.view('/api/test', 'text/html')
    def api_test(request):
        if request.method == 'GET':
	       return f'<h1>Your name must be {request.get("username")}</h1>'
        elif request.method == 'POST':
	       return f'<h1>Your name must be {request.post("username")}</h1>'
        else:
            return HTTPResponse(data='method not allowed', status=405)

Furthermore, pigeon supports *dynamic path arguments*, these allow for requests to include arguments inside the path.
This is probably best shown in an example::

    @app.view('/api/user/{{param1}}/view')
    def api_view_user(request, dynamic_params):
        if request.method == 'GET':
            print(f'The user is {dynamic_params.param1}')
            return f'<h1>You requested to view {dynamic_params.param1}!</h1>'
        else:
            return HTTPResponse(data='method not allowed', status=405)

Dynamic path arguments are indicated in the path by being enclosed in double curly brackets and can be accessed via an extra dynamic_params argument.
| Manually crafting error responses can be tideous, as such, there is a builtin function that can be used to generate error responses with the provided status code::

    from pigeon.shortcuts import error

    @app.view('/api/user/{{param1}}/view')
    def api_view_user(request, dynamic_params):
        if request.method == 'GET':
            print(f'The user is {dynamic_params.param1}')
            return f'<h1>You requested to view {dynamic_params.param1}!</h1>'
        else:
            # method not allowed
            return error(405)

Error responses will be generated using an error view that closely resembles a regular view. Depending on the status code provided to the function, a corresponding error view will be invoked.
We can define our own custom error view using `app.error`::

    @app.error(500)
    def internal_server_error(request):
	   return '<h1>Internal Server Error 500</h1>'

If no specific error view exists for a status code, the fallback error view with the code 0 will be used.
Like any other, the default fallback error view can also be overwritten::

    @app.error(0)
    def fallback_error(request, code):
        return f'<h1>No error view exists error {code}</h1>'


Changing Defualt Settings
-------------------------
If you wish to modify settings, you can achieve this through the Pigeon class.
You have the option to either override default settings by importing a module, overwrite them using a dictionary, or adjust them individually one by one::

    from pigeon import Pigeon
    from pathlib import Path

    # directory of project
    BASE_DIR = pathlib.Path(__file__).parent.resolve()

    app = Pigeon()

    # override settings from imported module
    import mysettings
    app.settings.override(mysettings)

    # override settigns using dictionary
    mysettings = {
        'VERBOSITY':  3,
        'PORT': 3000,
        'STATIC_URL_BASE': '/static/'
        'STATIC_FILES_DIR': BASE_DIR / 'static/'
    }

    # change settings manually
    app.settings.verbosity = 2
    app.port = 2556
    app.static_url_base = '/files/static/'
    app.static_files_dir = BASE_DIR / 'resources/static/'

The imported settings module should resemble the following::

    # settings.py

    VERBOSITY = 4
    PORT = 8080
    ALLOWED_HOSTS = ['teamsmiley.org']

The recommended approach for overriding default values is to modify the settings as demonstrated above.
Altering settings at runtime is not recommended as it might result in unpredictable and untested behavior.
A list of all available settings can be found :ref:`here <api.settings>`.

.. _tutorial.mediafiles:

Media Files
-----------
Media files refer to non-executable files such as images, vides, aufo files, etc., which are used within a web application.
They are primarily intended for user-generated content and should not be employed for crucial files required for the application's frontend.

By configuring the *MEDIA_URL_BASE* and *MEDIA_FILES_DIR* settings you automatically enable media files::

    from pigeon import Pigeon
    from pathlib import Path

    # directory of project
    BASE_DIR = pathlib.Path(__file__).parent.resolve()

    app = Pigeon()

    # enable staticfiles
    app.settings.media_url_base = '/media/'
    app.settings.media_files_dir = BASE_DIR / 'media/'

Let's consider the following project structure::

    .
    ├── app.py
    └── media
        └── img.png

After running the application we can access the img in our media folder under *http://localhost:8080/media/img.png*:

.. image:: ../_static/pages/tutorial/media_showcase.png
    :align: left
    :width: 100%

.. _tutorial.staticfiles:

Static Files
------------
Static files should be used for files such as CSS, JavaScript, images, and other assets that are essential for rendering the frontend of a web application.
Unlike media files, static files are typically not user-generated and should remain constant throughout the application's lifespan.
Pigeon will automatically load smaller static files into memory to allow for faster response times.

Much like media files, the handling of static files is effortlessly facilitated by configuring the *STATIC_URL_BASE* and *STATIC_FILES_DIR* settings.
By configuring these settings, static files will be automatically enabled::

    from pigeon import Pigeon
    from pathlib import Path

    # directory of project
    BASE_DIR = pathlib.Path(__file__).parent.resolve()

    app = Pigeon()

    # enable staticfiles
    app.settings.static_url_base = '/static/'
    app.settings.static_files_dir = BASE_DIR / 'static/'

Let's consider the following project structure::

    .
    ├── app.py
    └── static
        └── style.css

When running the application we access the css stylesheet under *http://localhost:8080/static/style.css*:

.. image:: ../_static/pages/tutorial/static_showcase.png
    :align: left
    :width: 100%