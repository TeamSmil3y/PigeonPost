import pigeon
from pigeon.utils.logger import create_log
import resources.settings as settings
from pathlib import Path
import os
import importlib.util
import sys

TESTS_DIR = Path(__file__).parent.resolve()

log = create_log('TESTRUNNER', 'green')


def configure_environment():
    # override default settings with settings for test environment
    pigeon.conf.manager.override(settings)
    # call manager.setup to configure runtime computed settings
    pigeon.conf.manager.setup()


def gather_tests(directory=TESTS_DIR, modules=[]):
    """
    Returns all test modules that are inside of any child package relative to <TEST_DIR>
    """
    packages = []
    # try to find any test packages which are childreen to this package
    for f in os.scandir(directory):
        if os.path.exists(Path(f.path)/'__init__.py'):
            log(3, f'FOUND PACKAGE {os.path.relpath(f.path, TESTS_DIR)}', color='blue', noprefix=True)
            # add current package
            packages.append(f)
            # find all python modules in package
            package_modules = gather_test_modules(f)
            modules += package_modules
            for module in package_modules:
                log(3, f'-> FOUND {os.path.relpath(module[0], TESTS_DIR)}', color='green', noprefix=True)
            
            # search children of package
            packages.append(gather_tests(f, modules))
            
    return modules


def gather_test_modules(package):
    """
    Fins all modules inside of the package that use unittest.
    """
    modules = []
    for f in os.scandir(package.path):
        path = f.path
        if f.is_file() and path.endswith('.py'):
            module = import_module(path)
            if hasattr(module, 'unittest'):
                modules.append((path, module))
    return modules


def import_module(path):
    # import module using path
    spec = importlib.util.spec_from_file_location(path, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_test(test):
    path, module = test
    log(3, f'RUNNING {path}', color='yellow', noprefix=True)
    module.unittest.main(module=module)


def main():
    log(2, 'CONFIGURING ENVIRONMENT')
    configure_environment()
    
    log(2, 'GATHERING TESTS')
    tests = gather_tests()

    log(2, 'RUNNING TESTS..')
    for test in tests:
        run_test(test)


if __name__ == '__main__':
    main()
