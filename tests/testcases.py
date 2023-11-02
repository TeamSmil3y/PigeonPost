import unittest
import runner


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        runner.log(3, f'RESTORING ENVIRONMENT', noprefix=True, color='yellow')
        runner.restore_environment()
        runner.log(3, f'RUNNING {cls.__module__}.{cls.__name__}', color='yellow', noprefix=True)
        # call child class func set_up_class
        if hasattr(cls, 'set_up_class'):
            cls.set_up_class()

    def setUp(self):
        # call child class func set_up
        if hasattr(self, 'set_up'):
            self.set_up()
    