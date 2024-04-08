[<img src="https://github.com/TeamSmil3y/PigeonPost/assets/52998857/283dc7d0-3aae-46b8-b255-1fa7b3b67699" />](https://docs.pigeon.teamsmiley.org)

# pigeon
Pigeon is a versatile Python web application framework. It prioritizes a seamless and straightforward initial setup process, while also providing the capability to develop sophisticated applications.

Pigeon is committed to empowering developers with complete control and an array of customization possibilities, all while ensuring user-friendly, convenient, and accessible usage.

## Getting Started
First install the current version of **[pigeonpost](https://pypi.org/project/pigeonpost/)** from PiPy:
```bash
$ python3 -m pip install pigeonpost
```

With pigeon installed we can now start writing our own application:
```python3
form pigeon import Pigeon

Pigeon()

@view('/')
def home(request):
    return '<h1> Hello World! </h1>'
```

## Features
- serve static files
- easy request and response handling
- use jinja2 templating engine

### Natively Supported Mimetypes:
- application/json
- multipart/form-data
- application/x-www-form-urlencoded
