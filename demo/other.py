from pigeon import Pigeon
from pigeon.shortcuts import HTTPResponse

@Pigeon.view('/welcome', 'application/json')
def welcome(request):
    return {'welcome': 'Hello World!'}

@Pigeon.view('/welcome', 'text/plain')
def welcome(request):
    return HTTPResponse(data='Welcome! Hello World!', content_type='text/plain')


@Pigeon.view('/goodbye', 'application/json')
def welcome(request):
    return {'cya': 'Bye World!'}


@Pigeon.view('/will-fail')
def will_fail(request):
    # this view will fail and cause error 500 (internal server error)
    return None
