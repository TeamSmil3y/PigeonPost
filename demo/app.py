from pigeon.shortcuts import HTTPResponse, JSONResponse, render
from pigeon import Pigeon
import settings

app = Pigeon(settings)


@app.view('/welcome', 'application/json')
def welcome(request):
    return {'welcome': 'Hello World!'}


@app.view('/welcome', 'text/plain')
def welcome(request):
    return HTTPResponse(data='Welcome! Hello World!', content_type='text/plain')


@app.view('/')
def counter(request):
    return render('counter.html', context={'request': request})
