# first pigeon setup
from pigeon import Pigeon
import settings

Pigeon(settings)
Pigeon.settings.port = 4001

# import of other modules
from pigeon.shortcuts import HTTPResponse, render
import errors, other, models

@Pigeon.view('/')
def counter(request):
    return render('counter.html', context={'request': request})

@Pigeon.view('/auth/', auth='Basic')
def authed(request):
    return f'<h1> Username: {request.auth.username} </h1><br/><h1> Password: {request.auth.password} </h1>'
