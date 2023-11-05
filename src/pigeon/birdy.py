import atexit
from typing import Callable
import pigeon.conf.manager as manager
import pigeon.core.server as server
import pigeon.middleware.views as views
import pigeon.utils.logger as logger

log = logger.Log('PIGEON', '#30b3ff')


class Pigeon:

    view_handler = None
    error_handler = None

    @classmethod
    def __init__(cls, settings=None):
        log.info('STARTING..')
        # overwrite standard settings if new settings provided
        if settings:
            manager.override(settings)

        # set
        manager.settings.pigeon = cls

        # view handlers
        cls.view_handler = views.ViewHandler()
        cls.error_handler = views.ErrorHandler()
        
        # configure runtime settings
        manager.setup()

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
    def view(cls, target: str, mimetype: str='*/*') -> Callable:
        def wrapper(func) -> Callable:
            log.debug(f'FOUND VIEW: ')
            log.sublog(f'TARGET: {target}:\nMIMETYPE: {mimetype}\nFUNC: {func}')
            # add to views
            cls.view_handler.register(target, func, mimetype)
            return func
        return wrapper
    
    # @decorator register error view
    @classmethod
    def error(cls, code) -> Callable:
        def wrapper(func) -> Callable:
            # add to error views
            cls.error_handler.register(code, func)
            return func
        return wrapper
