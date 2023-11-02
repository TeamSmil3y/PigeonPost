from pigeon.shortcuts import HTTPResponse, JSONResponse, render
from pigeon.decorators import content_type


@content_type('application/json')
def welcome(request):
    return JSONResponse(data={'welcome': 'Hello World!'})


@content_type('text/plain')
def welcome(request):
    return HTTPResponse(data='Welcome! Hello World!', headers={'Content-Type': 'text/plain'})


def counter(request):
    return render('counter.html', context={'request': request})
