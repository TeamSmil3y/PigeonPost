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
    0: COLORS['red'] + 'ERROR\t',
    1: COLORS['yellow'] + 'WARNING\t',
    2: COLORS['blue'] + 'INFO\t',
    3: COLORS['pink'] + 'VERBOSE\t',
    4: COLORS['pink'] + 'DEBUG\t',

}


def _log(logtype, msg, prefix='', end='\n', name=''):
    print(f'{prefix}{LOGTYPES[logtype]}{name} {msg}', end=end)


def anonlog(logtype, msg, prefix='', end='\n'):
    _log(logtype, msg, prefix, end)


def create_log(name, color):
    name = COLORS['grey'] + '[' + COLORS[color] + name + COLORS['grey'] + ']' + COLORS['white']
    return lambda logtype, msg, prefix='', end='\n': _log(logtype, msg, prefix, end, name)
