import os
import sys

# gather all previously imported modules for watchdog (debug mode)
# doing this before importing all other modules reduces files that will be monitored by watchdog
modules = sys.modules.values()
import pigeon.conf

pigeon.conf.Manager.module_dirs = []
for module in modules:
    if module.__name__ not in sys.builtin_module_names and module.__name__ not in sys.stdlib_module_names and \
            hasattr(module, '__file__') and module.__file__ and \
            'site-packages' not in (module_path := os.path.dirname(module.__file__)):
        pigeon.conf.Manager.module_dirs.append(module_path)

from pigeon.core.app import Pigeon
import pigeon.core
import pigeon.database
import pigeon.files
import pigeon.http
import pigeon.templating
import pigeon.utils
import pigeon.middleware
