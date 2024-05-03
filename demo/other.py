from pigeon import Pigeon
from pigeon.shortcuts import HTTPResponse

@Pigeon.view('/welcome', 'application/json')
def welcome(request):
    return {'welcome': 'Hello World!'}

@Pigeon.view('/welcome', 'text/plain')
def welcome(request):
    return HTTPResponse(data='Welcome! Hello World!', content_type='text/plain')


@Pigeon.view('/user/{{param1}}/view')
def api_view_user(request, dynamic_params):
    if request.method == 'GET':
        return f'<h1>You requested to view {dynamic_params.param1}!</h1>'
    return HTTPResponse(data='method not allowed', status=405, content_type='text/plain')


@Pigeon.view('/goodbye', 'application/json')
def welcome(request):
    return {'cya': 'Bye World!'}


@Pigeon.view('/will-fail')
def will_fail(request):
    # this view will fail and cause error 500 (internal server error)
    return None
