Quickstart
==========


Installation
------------
PigeonPost is available on:
 * PiPy

To install from PiPy, run:

.. code-block:: shell

    $ python3 -m pip install pigeonpost


Getting Started
---------------
With pigeon installed, we can create a simple working web application like:

.. code-block:: python

    from pigeon import Pigeon
    app = Pigeon()

    @app.view('/')
    def home(request):
        return '<h1>Hello World!</h1>'

    @app.view('/welcome')
    def welcome(request):
        return HTTPResponse(data='Welcome!')

Normal views should allways return either HTTPResponse objects or strings.
We can also add *typed views* by passing the mimetype of our view as the second argument for app.view.
Pigeon will automatically choose the most fitting typed view for the requested path depending on the `Accept` header:

.. code-block:: python

    from pigeon.shortcuts import HTTPResponse, JSONResponse
    import json

    @app.view('/api/test', 'application/json')
    def api_test(request):
        return HTTPResponse(data=json.dumps({'Hello':'World!'}))

    @app.view('/api/test', 'text/plain')
    def api_test(request):
        return HTTPResponse(data='Hello World!')

In contrast to normal views, typed views supports automatic conversion of return data to HTTPResponse objects.
This means that a view with the mimetype `application/json` can return any JSON convertible data such as dicts, list, ...:

.. code-block:: python

    @app.view('/api/test', 'application/json')
    def api_test(request):
        return {'this data is':'autoconverted to an HTTPResponse object'}

If we want to process data provided in the request, we can use the `get`, `data`, and `files` functions:

.. code-block:: python

    @app.view('/api/test', 'text/html')
    def api_test(request):
        if request.method == 'GET':
	       return f'<h1>Your name must be {request.get("username")}</h1>'
        elif request.method == 'POST':
	       return f'<h1>Your name must be {request.post("username")}</h1>'
        else:
            return HTTPResponse(data='method not allowed', status=405)

Furthermore, pigeon supports *dynamic path arguments*, these allow for requests to include arguments inside the path.
This is probably best shown in an example:

.. code-block:: python

    @app.view('/api/user/{{param1}}/view')
    def api_view_user(request, dynamic_params):
        print(f'The user is {dynamic_params.param1}')
        return f'<h1>You requested to view {dynamic_params.param1}!</h1>'

Dynamic path arguments are indicated in the path by being enclosed in double curly brackets and can be accessed via an extra dynamic_params argument.
