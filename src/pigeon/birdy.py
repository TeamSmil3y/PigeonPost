import re
import pigeon.conf.manager as manager
import pigeon.core.server as server
from pigeon.utils.loggger import Log

log = Log('PIGEON', '#30b3ff')


class Pigeon:
    def __init__(self, settings=None):
        log.info('')
        # overwrite standard settings if new settings provided
        if settings:
            manager.override(settings=settings)

        # view handlers
        self.view_handler = module.module.ViewHandler()
        self.error_handler = module.module.ErrorHandler()
        
        # configure runtime settings
        manager.setup()
        manager.settings.VIEWHANDLER = self.view_handler
        
        # run application
        self.run()
        
    def run(self):
        log.info('STARTING SERVER')
        # start server
        server.start()
        server.serve()

    # DECORATORS:
    # ===========

    # register view
    def view(self, target: str, mimetype: str='*/*'):
        
        if re.search('.*{{.*}}.*', target):
            # has dynamic params
            ...
        
        def wrapper(func):
            print(f'[REMOVE THIS] VIEW {target}/{mimetype} -> {func}')
            # add to views
            self.view_handler.register(target, func, mimetype)
        return wrapper
    
    # register error view
    def error(self, code):
        def wrapper(func):
            # add to error views
            self.error_handler.register(code, func)
        return wrapper
