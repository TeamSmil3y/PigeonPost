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
With pigeon installed, we can create a new project like::

    $ python3 -m pigeonpost create myProject

This creates the following folder structure::

    .
    ├── myApp.py
    ├── settings.py

Inside `settings.py` we can now configure any settings related to the web application such as the address, port, views, static files, media files, templating, parsers, ...
Once you are ready to start your application simply run::

    $ python3 myApp.py
