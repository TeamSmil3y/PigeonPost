from pigeon import Pigeon
from pigeon.shortcuts import HTTPResponse, render
import settings

app = Pigeon(settings)
app.settings.port = 4001

@app.view('/welcome', 'application/json')
def welcome(request):
    return {'welcome': 'Hello World!'}


@app.view('/welcome', 'text/plain')
def welcome(request):
    return HTTPResponse(data='Welcome! Hello World!', content_type='text/plain')


@app.view('/dynamic/{{user}}/display')
def counter(request, dynamic):
    return f'<h1>{dynamic.user}</h1>'


@app.view('/')
def counter(request):
    return render('counter.html', context={'request': request})

@app.view('/auth/', auth='Basic')
def authed(request):
    return f'<h1> Username: {request.auth.username} </h1><br/><h1> Password: {request.auth.password} </h1>'
