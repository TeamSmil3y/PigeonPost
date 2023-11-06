Tutorial
========

Views
-----
Views are functions that correspod to a certain request pawth or route on the web application.
The view \'\/welcome\' would could be requested by visiting the url *http://my-app:8080/welcome*

Typing
******
Pigoen supports typing of views.
This a allows us to add a return `mimetype <https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types>`_ which will be used for server-driven content negotiation.
Essentially, this enables us to allow the client to specify the desired mimetype for the server response.

    While typing is supported by pigeon, it is not required.
    Views that do not specify a mimetype will default to \*/\* (any mimetype).

Untyped Views
*************
Any view with the mimetype \*/\* is considered untyped.
Untyped views are expected to return either HTTPResponse objects or strings::

    from pigeon import Pigeon
    app = Pigeon()

    @app.view('/')
    def home(request):
        return '<h1>Hello World!</h1>'

    @app.view('/welcome')
    def welcome(request):
        return HTTPResponse(data='Welcome!')

Typed Views
***********
To make a view typed, we can add the mimetype of our view as the second argument for `app.view`.
Pigeon will automatically select the most fitting typed view for any incoming the request::

    from pigeon.shortcuts import HTTPResponse, JSONResponse
    import json

    @app.view('/api/test', 'application/json')
    def api_test(request):
        return HTTPResponse(data=json.dumps({'Hello':'World!'}))

    @app.view('/api/test', 'text/plain')
    def api_test(request):
        return HTTPResponse(data='Hello World!')

Unlike regular views, typed views offer automatic conversion of return data into HTTPResponse objects.
This means that a view with the mimetype application/json can effortlessly return any JSON-compatible data, including dictionaries, lists, and more::

    @app.view('/api/test', 'application/json')
    def api_test(request):
        return {'this data is':'autoconverted to an HTTPResponse object'}

If we need to retrieve data provided in the request, we can utilize the get, data, and files functions::

    @app.view('/api/test', 'text/html')
    def api_test(request):
        if request.method == 'GET':
	       return f'<h1>Your name must be {request.get("username")}</h1>'
        elif request.method == 'POST':
	       return f'<h1>Your name must be {request.post("username")}</h1>'
        else:
            return HTTPResponse(data='method not allowed', status=405)

Dynamic Path Arguments
**********************
Additionally, Pigeon supports dynamic path arguments, which enable requests to include arguments within the path.
Dynamic path arguments are denoted in the path by being enclosed in double curly brackets and can be accessed via an additional dynamic_params argument.
This is best demonstrated through an example::

    @app.view('/api/user/{{param1}}/view')
    def api_view_user(request, dynamic_params):
        if request.method == 'GET':
            print(f'The user is {dynamic_params.param1}')
            return f'<h1>You requested to view {dynamic_params.param1}!</h1>'
        else:
            return HTTPResponse(data='method not allowed', status=405)

Error Responses
***************
Crafting error responses manually can be a time-consuming task. To simplify this process, Pigeon offers a built-in function that automatically generates error responses based on the provided status code::

    from pigeon.shortcuts import error

    @app.view('/api/user/{{param1}}/view')
    def api_view_user(request, dynamic_params):
        if request.method == 'GET':
            print(f'The user is {dynamic_params.param1}')
            return f'<h1>You requested to view {dynamic_params.param1}!</h1>'
        else:
            # method not allowed
            return error(405)

Overriding default Error Responses
**********************************
When calling the error function, Pigeon will try to locate a matching error view to generate the response.
In case no error view matches the provided status code, a fallback will be invoked.

Error views closely resemble regular untyped views.
We have the ability to define our own custom error view using app.error::

    @app.error(500)
    def internal_server_error(request):
	   return '<h1>Internal Server Error 500</h1>'

The error fallback is set to match the unused status code 0.
Similar to any other error view, the default fallback error view can also be overridden::

    @app.error(0)
    def fallback_error(request, code):
        return f'<h1>No error view exists error {code}</h1>'


Configuring Settings
--------------------
If we wish to modify settings, we can achieve this through the Pigeon class.
We have the option to either override default settings by importing a module, overwrite them using a dictionary, or adjust them individually one by one::

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

By configuring the *MEDIA_URL_BASE* and *MEDIA_FILES_DIR* settings we automatically enable media files::

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

 .. _tutorial.templating:

Templating
----------
Templates serve as pre-defined structures that allow us to dynamically generate HTML content.
They act as placeholders where dynamic data can be inserted before sending a response to a client's request.

Pigeon uses the jinja2 templating engine.
If you want to learn how to make your own templates, the documentation for writing jinja2 templates can be found `here <https://jinja.palletsprojects.com/en/3.1.x/templates/>`_.

To enable templates, we must specify a template directory using the *TEMPLATES_DIR* setting, which will automatically activate them.
It is important to ensure that all our templates are located within this designated directory, as otherwise, Pigeon will not be able to locate them::

    from pigeon import Pigeon
    from pathlib import Path

    # directory of project
    BASE_DIR = pathlib.Path(__file__).parent.resolve()

    app = Pigeon()

    # configure templates directory
    app.settings.templates_dir = BASE_DIR / 'templates/'

To make use of the templates we can utilize the *render* function::

    from pigeon.shortcuts import render

    @app.view('/thisisrendered/')
    def my_rendered_view(request):
        return render('path/to/template.html', context={'request':request})

