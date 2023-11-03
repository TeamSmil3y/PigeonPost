<img src="https://github.com/TeamSmil3y/PigeonPost/blob/main/demo/media/img/pigeonpost.png?raw=true" alt="icon could not be loaded" style="width: 2em; " align="left" />
Simple and easy to use Python web framework

# pigeon
Pigeon is a versatile standalone Python web application framework. It prioritizes a seamless and straightforward initial setup process, while also providing the capability to develop sophisticated applications.

Pigeon is committed to empowering developers with complete control and an array of customization possibilities, all while ensuring user-friendly, convenient, and accessible usage.

## Getting Started
First install the current version of **[pigeonpost](https://pypi.org/project/pigeonpost/)** from PiPy:
```bash
$ python3 -m pip install pigeonpost
```
Now that pigeonpost is installed, we can create a new project:
```bash
$ python3 -m pigeonpost create myApp
```
This creates the following project structure:
```
.
├── myApp.py
├── settings.py
```
Inside `settings.py` you can configure all settings related to the web application such as the address, port, views, static files, media files, templating, parsers, ...
Once you are ready to start your application simply run:
```bash
$ python3 myApp.py
```

## Features
- serve static files
- easy request and response handling
- use jinja2 templating engine

### Natively Supported Mimetypes:
- application/json
- multipart/form-data
- application/x-www-form-urlencoded
