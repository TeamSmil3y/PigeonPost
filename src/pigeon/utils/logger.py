import threading


TOTAL_PREFIX_LENGTH = 50
VERBOSITY = 4
COLORS = {
    'white': '\033[39m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'green': '\033[92m',
    'blue': '\033[94m',
    'cyan': '\033[96m',
    'pink': '\033[95m',
    'grey': '\033[97m',
}

LOGTYPES = {
    0: COLORS['red'] + 'ERROR   ',
    1: COLORS['yellow'] + 'WARNING ',
    2: COLORS['blue'] + 'INFO    ',
    3: COLORS['pink'] + 'VERBOSE ',
    4: COLORS['pink'] + 'DEBUG   ',

}

lock = threading.Lock()


def _log(logtype, *args, prefix='', end='\n', name='', subname=''):
    if logtype <= VERBOSITY:
        _prefix = f'{prefix}{LOGTYPES[logtype]}{name}{("-" + subname) if subname else ""}'
        _prefix = _prefix[:TOTAL_PREFIX_LENGTH] + ' ' * (TOTAL_PREFIX_LENGTH-len(_prefix)) + COLORS['white'] + ' '
        with lock:
            print(_prefix, *args, end=end)


def anonlog(logtype, msg, prefix='', end='\n'):
    _log(logtype, msg, prefix, end)


def create_log(name, color, subname=''):
    name = COLORS['grey'] + '[' + COLORS[color] + name + COLORS['grey'] + ']'
    _subname = subname
    return lambda logtype, *args, prefix='', end='\n', subname=_subname: _log(logtype, *args, prefix=prefix, end=end, name=name, subname=subname)
