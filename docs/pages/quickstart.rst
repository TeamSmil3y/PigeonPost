Quickstart
==========


Installation
------------
PigeonPost is available on:
 * PiPy

To install from PiPy, run::

    $ python3 -m pip install pigeonpost


Getting Started
---------------
With pigeon installed, we can create a simple working web application like::

    from pigeon import Pigeon
    app = Pigeon()

    @app.view('/')
    def home(request):
        return '<h1>Hello World!</h1>'

    @app.view('/welcome')
    def welcome(request):
        return HTTPResponse(data='Welcome!')

Normal views should allways return either HTTPResponse objects or strings.
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

Manually crafting error responses can be tideous, as such, there is a builtin function that can be used to generate error responses with the provided status code::

    from pigeon.shortcuts import error

    @app.view('/api/user/{{param1}}/view')
    def api_view_user(request, dynamic_params):
        if request.method == 'GET':
            print(f'The user is {dynamic_params.param1}')
            return f'<h1>You requested to view {dynamic_params.param1}!</h1>'
        else:
            # method not allowed
            return error(405)

The error responses will be generated using an error view which is very similar to a regular view.
Depending on the status code we pass to the function a different error view will be called.
We can define our own error view using `app.error`::

    @app.error(500)
    def internal_server_error(request):
	   return '<h1>Internal Server Error 500</h1>'

 If no specific error view exists for a status code, the fallback error view with the code 0 will be used.
 Like any other, the default fallback error view can also be overwritten::

    @app.error(0)
    def fallback_error(request, code):
        return f'<h1>No error view exists error {code}</h1>'

