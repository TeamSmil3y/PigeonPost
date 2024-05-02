import io
import threading
import rich
from pigeon.conf import Manager

lock = threading.Lock()
print = rich.get_console().print


class Log:
    # max length of name
    max_name_length = 15
    # color subnames will be displayed in
    off_color = '[#8888aa]'

    def __init__(self, name, color='#ffffff', subname=''):
        self.name = name
        self.color = color
        self.default_subname = subname
        self.color_length = len(self.color)+10+len(self.off_color)*2
        # whether the last message was blocked due to verbosity level
        self.message_blocked = False

    def _build_prefix(self, subname):
        # determine prefix length
        subname = subname or self.default_subname
        if subname: subname = '-'+subname

        prefix = f'{self.off_color}[[/][{self.color}]{self.name}[/]{self.off_color}]{subname}'
        prefix = prefix[:self.max_name_length+self.color_length] + ' ' * (self.max_name_length-len(prefix)+self.color_length)
        prefix += '[/]  '
        return prefix

    def _print_msg(self, *args, end, subname):
        print(self._build_prefix(subname), *args, end=end)

    def critical(self, *args, end='\n', subname=''):
        self.message_blocked = False
        with lock:
            print('[bold red]CRITICAL [/]', end='')
            self._print_msg(*args, end=end, subname=subname)

    def error(self, *args, end='\n', subname=''):
        self.message_blocked = False
        with lock:
            print('[#ffaaaa]ERROR    [/]', end='')
            self._print_msg(*args, end=end, subname=subname)

    def warning(self, *args, end='\n', subname=''):
        self.message_blocked = False
        with lock:
            print('[#ffff99]WARNING  [/]', end='')
            self._print_msg(*args, end=end, subname=subname)

    def info(self, *args, end='\n', subname=''):
        self.message_blocked = Manager.verbosity < 2
        if not self.message_blocked:
            with lock:
                print('[#5555ff]INFO     [/]', end='')
                self._print_msg(*args, end=end, subname=subname)

    def verbose(self, *args, end='\n', subname=''):
        self.message_blocked = Manager.verbosity < 3
        if not self.message_blocked:
            with lock:
                print('[#ffaaff]VERBOSE  [/]', end='')
                self._print_msg(*args, end=end, subname=subname)

    def debug(self, *args, prefix='', end='\n', subname=''):
        self.message_blocked = Manager.verbosity < 4
        if not self.message_blocked:
            with lock:
                print('[#ffaaff]DEBUG    [/]', end='')
                self._print_msg(*args, end=end, subname=subname)

    def sublog(self, *args, color='white][/', end='\n'):
        """
        For log messages that give extra context and details on the previous logmessage.
        They will only be logged if the previous log message was logged as well.
        """
        if not self.message_blocked:
            with lock:
                msg = ''
                for arg in args: msg += arg
                msg = msg.replace('\n', self.off_color+'\n│   [/]['+color+']')
                print(f'{self.off_color}├─  [/]', end='')
                print('['+color+']'+msg+('[/]' if color!='white][/' else ''))
