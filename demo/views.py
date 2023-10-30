from pigeon.shortcuts import JSONResponse, render

def welcome(request):
    return JSONResponse(data={'welcome':'Hello World!'})

def counter(request):
    return render('counter.html', context={'request': request})