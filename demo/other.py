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

