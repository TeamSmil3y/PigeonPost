Quickstart
==========


Installation
------------
PigeonPost is available on:
 * PiPy

To install on PiPy, run::

    $ python3 -m pip install pigeonpost


Getting Started
---------------
With pigeon installed, we can create a simple working web application like::

    from pigeon import Pigeon
    app = Pigeon()

    @app.view('/')
    def home(request):
	return '<h1>Hello World!</h1>'
