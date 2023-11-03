import unittest
import runner
from pigeon.utils.logger import sublog


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        runner.log.sublog(f'RESTORING ENVIRONMENT', color='yellow')
        runner.restore_environment()
        runner.log.sublog(f'RUNNING TEST:\n\t{cls.__module__}.{cls.__name__}', color='yellow')
        # call child class func set_up_class
        if hasattr(cls, 'set_up_class'):
            cls.set_up_class()

    def setUp(self):
        # call child class func set_up
        if hasattr(self, 'set_up'):
            self.set_up()
    