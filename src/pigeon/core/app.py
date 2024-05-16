import atexit
import sys
import os
import traceback
from typing import Callable
from pigeon.conf import Manager
import pigeon.core.server as server
import pigeon.middleware.views as views
import pigeon.middleware.auth as auth
import pigeon.utils.logger as logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

log = logger.Log('PIGEON', '#30b3ff')

class Pigeon:
    """
    The Pigeon class is the main interface used for the user to interact with Pigeon.
    It houses important decorators for registering views, etc. such as Pigeon.view and Pigeon.error.

    Furthermore it facilitates exception-handling, exit-handling, debug_mode application
    reinitialization through watchdog,
    """

    settings = None
    autorun = True

    # watchdog
    observers = []
    @classmethod
    def __init__(cls, settings=None):
        """
        On initialization, pigeon performs a few important actions, mainly:
        - sets up the pigeon.conf.manager.Manager class.
        - default sys.excepthook and sys.exit handlers are set to pigeons custom exception handler and exit handler.
        - registers Pigeon.run to execute at the normal exit of a program, i.e. after all other code has executed,
        using the atexit hook
        """
        log.info('STARTING..')

        # overwrite standard settings if new settings provided
        if settings:
            Manager.override(settings)

        # view handlers
        Manager.view_handler = views.ViewHandler()
        Manager.error_handler = views.ErrorHandler()
        # auth handlers
        Manager.auth_handler = auth.AuthHandler()

        # shortcut
        cls.settings = Manager

        # configure runtime settings
        Manager._setup()

        # exception handling
        sys.excepthook = cls.handle_exception
        sys.exit = cls.handle_exit
        # run pigeon after everything has been configured (all decorators executed)
        atexit.register(Pigeon.run)

    @classmethod
    def run(cls, auto=False) -> None:
        """
        :param auto: specifies whether the application has been started automatically due to the atexit call,
        if so we will check back whether this
        """
        if Manager.debug_mode:
            log.debug('WATCHING MODULES FOR CHANGES: (DEBUG MODE)')
            for module in Manager.module_dirs:
                log.sublog(module)
            log.info('INITIALIZING WATCHDOG CONFIGURATION')
            event_handler = FileSystemEventHandler()

            def restart_event(event):
                cls.restart()

            event_handler.on_modified = restart_event
            for module in Manager.module_dirs:
                watchdog_observer = Observer()
                watchdog_observer.schedule(event_handler, path=module, recursive=False)
                watchdog_observer.start()
                cls.observers.append(watchdog_observer)

        if not cls.autorun:
            log.verbose("AUTORUN DISABLED - SKIPPING")
            return

        cls.autorun = False

        log.info('STARTING')
        try:
            # start server
            server.start()
            server.serve()
        except PermissionError as e:
            if e.errno == 13: log.critical("PERMISSION DENIED (PORTS 0-1024 REQUIRE ADMINISTRATIVE PRIVILEGES)")
        except OSError as e:
            if e.errno == 98: log.critical("ADDRESS ALREADY IN USE")

    @classmethod
    def restart(cls):
        """
        Restarts the entire application
        """
        log.info("RESTARTING THE APPLICATION")
        os.execl(sys.executable, sys.executable, *sys.argv)

    @classmethod
    def handle_exception(cls, exception_type, exception, *args, custom_log: logger.Log = log, description: str='AN EXCEPTION OCCURED') -> None:
        """
        :param exception_type: Type of exception (unused)
        :param exception: The exception that should be handled
        :param custom_log: Pigeon log that error message corresponding to the exception will be logged in
        :param description: The status message that will be logged to explain or give details about the error

        This is a custom exception handler. It facilitates the following:

        * if an exception occurs before the server has started, the server will not start
        * exceptions during runtime will be logged and if the CRASH_ON_FAILURE setting is set to True the app will terminate

        """
        sys.last_exc = exception
        custom_log.error(description)
        custom_log.sublog(''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))[:-1])

        if cls.autorun:
            log.critical("AN EXCEPTION OCCURED BEFORE PIGEON STARTED, AUTORUN WILL BE DISABLED")
            cls.autorun = False

        if Manager.crash_on_failure:
            log.critical("CRASH ON FAILURE ACTIVE - TERMINATING")
            sys.exit(-1)

    @classmethod
    def handle_exit(cls, status, force: bool = False) -> None:
        if force or Manager.crash_on_failure:
            log.info("EXITING")
            os._exit(status)

    # @decorator register view
    @classmethod
    def view(cls, target: str, mimetype: str='*/*', auth=None) -> Callable:
        def wrapper(func) -> Callable:
            log.debug(f'FOUND VIEW: ')
            log.sublog(f'TARGET: {target}:\nMIMETYPE: {mimetype}\nFUNC: {func}\nAUTH: {auth}')
            # add to views
            Manager.view_handler.register(target, func, mimetype, auth)
            return func
        return wrapper

    # @decorator register error view
    @classmethod
    def error(cls, code: int) -> Callable:
        def wrapper(func: Callable) -> Callable:
            # add to error views
            Manager.error_handler.register(code, func)
            return func
        return wrapper
