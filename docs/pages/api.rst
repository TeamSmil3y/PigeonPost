API
===

HTTPRequest and HTTPResponse
----------------------------
🚧 ..under construction... 🏗️

.. _api.settings:

Settings
--------
Below is a list of all available settings:

.. list-table:: available settings
   :widths: 1 1 2 1
   :header-rows: 1

   * - name
     - type
     - description
     - default
   * - VERBOSTIY
     - int
     - Verbosity of the logger. Recommended value is 2-3.
     - 2
   * - ADDRESS
     - str
     - Address for the web application. An empty string \'\' will allow requests to any available interface (any valid address).
     - \'\'
   * - PORT
     - int
     - Port number for the web application.
     - 8080
   * - ALLOWED_HOSTS
     - list[str, ...] | tuple[str, ...]
     - List of allowed host names for the web application. If set to [\'\*\'] all host names will be valid
     - [\'\*\']
   * - ALLOWED_METHODS
     - list[str, ...] | tuple[str, ...]
     - Methods that can be used in requests to webapp.
     - [\'POST\', \'GET\', \'HEAD\', \'POST\', \'PUT\', \'OPTIONS\']
   * - CORS_ALLOWED_ORIGINS
     - list[str, ...] | tuple[str, ...]
     - List of allowed origins for Cross-Origin Resource Sharing (CORS).
     - []
   * - CORS_ALLOW_CRED
     - bool
     - Whether to allow credentials in CORS requests.
     - False
   * - CORS_ALLOWED_HEADERS
     - list[str, ...] | tuple[str, ...]
     - List of allowed headers for CORS requests.
     - [\'Content-Type\']
   * - CORS_ALLOWED_METHODS
     - list[str, ...] | tuple[str, ...]
     - List of allowed HTTP methods for CORS requests.
     - [\'POST\', \'GET\', \'HEAD\', \'POST\', \'PUT\', \'OPTIONS\']
   * - CORS_MAX_AGE
     - int
     - Maximum age (in seconds) of the CORS preflight request.
     - 1200
   * - STATIC_URL_BASE
     - str
     - Base URL for serving static files. If not set, static files will be disabled.
     - None
   * - STATIC_FILES_DIR
     - pathlib.Path
     - Directory path for static files.
     - None
   * - MEDIA_URL_BASE
     - str
     - Base URL for serving media files. If not set, media files will be disabled.
     - None
   * - MEDIA_FILES_DIR
     - pathlib.Path
     - Directory path for media files.
     - None
   * - TEMPLATES_DIR
     - pathlib.Path
     - Directory path for templates.
     - None
   * - USE_HTTPS
     - bool
     - Whether to use HTTPS for the web application.
     - False
   * - CERTIFICATE_PATH
     - pathlib.Path
     - Path to the SSL certificate file.
     - None
   * - PRIVATE_KEY_PATH
     - pathlib.Path
     - Path to the private key file for HTTPS.
     - None
   * - PRIVATE_KEY_PASSWD
     - str
     - Password for the private key file (if encrypted). If no password is provided but one is required, Pigeon will prompt you to enter the password.
     - None
   * - MIME_PARSERS
     - dict[str : str]
     - Dictionary mapping MIME types to corresponding parsers (only for request body).
     - None
   * - MIME_GENERATORS
     - dict[str : str]
     - Dictionary mapping MIME types to corresponding generators (automatic conversion of typed views).
     - None
