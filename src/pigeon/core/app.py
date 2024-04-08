import atexit
from typing import Callable
from pigeon.conf import Manager
import pigeon.core.server as server
import pigeon.middleware.views as views
import pigeon.middleware.auth as auth
import pigeon.utils.logger as logger

log = logger.Log('PIGEON', '#30b3ff')


class Pigeon:

    settings = None

    @classmethod
    def __init__(cls, settings=None):
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

        # run pigeon after everything has been configured (all decorators executed)
        atexit.register(Pigeon.run)


    @classmethod
    def run(cls) -> None:
        log.info('STARTING SERVER')
        # start server
        server.start()
        server.serve()

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
