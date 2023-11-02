import threading


TOTAL_PREFIX_LENGTH = 50
VERBOSITY = 4
COLORS = {
    'white': '\033[39m',
    # dark colors
    'red': '\033[91m',
    'yellow': '\033[93m',
    'green': '\033[92m',
    'blue': '\033[94m',
    'cyan': '\033[96m',
    'pink': '\033[95m',
    'grey': '\033[97m',
    # light  colors
    'lred': '\033[31m',
    'lyellow': '\033[33m',
    'lgreen': '\033[32m',
    'lblue': '\033[34m',
    'lcyan': '\033[36m',
    'lpink': '\033[35m',
    'lgrey': '\033[37m',
}

LOGTYPES = {
    -1: COLORS['white'] + '        ',
    0: COLORS['red'] + 'ERROR   ',
    1: COLORS['yellow'] + 'WARNING ',
    2: COLORS['blue'] + 'INFO    ',
    3: COLORS['pink'] + 'VERBOSE ',
    4: COLORS['pink'] + 'DEBUG   ',
}

lock = threading.Lock()


def _log(logtype, *args, prefix='', end='\n', name='', subname='', noprefix=False, color='white'):
    if logtype <= VERBOSITY:
        _prefix = f'{prefix}{LOGTYPES[logtype]}{name}{("-" + subname) if subname else ""}'
        _prefix = _prefix[:TOTAL_PREFIX_LENGTH] + ' ' * (TOTAL_PREFIX_LENGTH-len(_prefix)) + COLORS['white'] + ' '
        if noprefix: _prefix = COLORS['grey']+' ├─ '+COLORS['white']
        with lock:
            print(_prefix + COLORS[color], end='')
            print(*args, COLORS['white'], end=end)


def anonlog(logtype, *args, prefix='', end='\n', noprefix=False, color='white'):
    _log(logtype, *args, prefix=prefix, end=end, noprefix=noprefix, color=color)


def create_log(name, color, subname=''):
    name = COLORS['grey'] + '[' + COLORS[color] + name + COLORS['grey'] + ']'
    def log(logtype, *args, prefix='', end='\n', subname=subname, noprefix=False, color='white'):
        _log(logtype,
             *args,
             prefix=prefix,
             end=end,
             name=name,
             subname=subname,
             noprefix=noprefix,
             color=color)
    return log
