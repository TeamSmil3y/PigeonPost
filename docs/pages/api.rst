API
===

Running Pigeon
--------------
Pigeon will runs at exit (using the `atexit`_ hook), i.e. it will start after all other code has been executed.
This provides some additional challenges, such as:

.. _atexit: https://docs.python.org/3/library/atexit.html

* different exception handling
* different exit handling

Exception Handling
******************
Pigeon uses a custom exception hook (overwriting `sys.excepthook`_), as exceptions that occur at normal interpreter termination are left unhandled.
The exception handler depending on the *CRASH_ON_FAILURE* setting calls `sys.exit`_ and
allways logs any exceptions using the default Pigeon logger.

The custom exception handler also provides the ability to pass two additional arguments, *log* and *description* which can
be used to log the exception in the context of another `Pigeon.utils.logger.Log`_ object and provide a custom description
for the exception that was raised::

    # assuming this is executing while Pigeon is already running
    import sys
    from Pigeon.shortcuts.logger import Log

    my_log = Log('Custom Log', color='red')

    my_exception = Exception("This is an Excpetion")
    sys.excepthook(None, my_exception, None, log=my_log, description='Hey look an Exception occured')

If the arguments *log* or *description* are not specified default values will be used.


.. _sys.excepthook: https://docs.python.org/3/library/sys.html#sys.excepthook
.. _sys.exit: https://docs.python.org/3/library/sys.html#sys.exit

Exit Handling
*************
The default exit handler at interpeter termination does not exit since the interpreter is already in the process of exiting.
Since this is not the desired behaviour Pigeon overwrites this exit handler with a custom handler, which terminates only if
either the *CRASH_ON_FAILURE* setting is set to *True* or the *Force* parameter of the function is set to *True*::

    # assuming this is executing while Pigeon is already running
    import sys

    # exit if CRASH_ON_FAILUE = True
    sys.exit(0)

    # force exit
    sys.exit(0, force=True)

.. _HTTPRequest and HTTPResponse:

HTTPRequest and HTTPResponse
----------------------------
🚧 ..under construction... 🏗️

.. _Pigeon.utils.logger.Log:

Pigeon Logging
--------------
The Pigeon logger is used for any logs that occur during runtime. It has different verbosity levels and depending on the
*VERBOSITY* setting a log will be printed or not:

.. list-table:: verbosity Levels
   :widths: 1 1 2
   :header-rows: 1

   * - name
     - verbosity level
     - usage
   * - critical
     - -1 (always)
     - Errors that cannot be ignored and will cause Pigeon to crash
   * - error
     - -1 (always)
     - Errors that may or may not cause Pigeon to crash
   * - warning
     - -1 (always)
     - Information important for Developers to improve their application, these should not be followed by a crash
   * - info
     - 1
     - Basic status messages explaining what is happening
   * - verbose
     - 2
     - Additional information about why certain actions are performed, etc.
   * - debug
     - 3
     - Messages explaining in detail everything that is happening (request, responses, ...)

Pigeon logging works by *registering* a log. Each log has a custom *name* and *color*. To register a log simply create
an object of the logger.Log class::

    from Pigeon.shortcuts.logger import Log

    my_log = Log('Custom Log', color='red')

    my_log.critical("This is a critical log message")
    my_log.error("This is an error message")
    my_log.warning("This is a warning")
    my_log.info("This is an information")
    my_log.verbose("This is a verbose message")
    my_log.debug("This is a debug message")

Furthermore Pigeon adds the ability to use *sublogs*, these are used to specify additional information regarding the
previously logged message. Sublogs will only be printed if the corresponding last log message was printed as well
according to the specified verbosity setting::

    from Pigeon.shortcuts.logger import Log

    my_log = Log('Custom Log', color='red')

    my_log.warning("Hey this is a warning!")
    my_log.sublog("You should be concerned!")

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
   * - CRASH_ON_FAILURE
     - bool
     - Whether to crash the server when an error occurs
     - False
   * - DEBUG_MODE
     - bool
     - Whether to activate debug mode
     - True
   * - MIME_PARSERS
     - dict[str : str]
     - Dictionary mapping MIME types to corresponding parsers (only for request body).
     - None
   * - MIME_GENERATORS
     - dict[str : str]
     - Dictionary mapping MIME types to corresponding generators (automatic conversion of typed views).
     - None
