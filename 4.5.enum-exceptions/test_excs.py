import unittest
from unittest import TestCase

from excs import EnumAppExceptions

from collections import namedtuple

class TestEnumAppExceptions(TestCase):
    
    def load_eg_AppExceptions(self):
        ExcArgs = namedtuple('ExcArgs','code exc_type message')
        self.dict_app_excs = dict(
            NotAnInteger = ExcArgs(1,TypeError,'Value is not an integer.'),
            OutOfRange = ExcArgs(2,ValueError,'Value is out of range.'),
            KeyNotFound = ExcArgs(3,KeyError,'Key was not found in hashable.')
        )
        class AppExceptions(EnumAppExceptions):
            NotAnInteger = self.dict_app_excs['NotAnInteger']
            OutOfRange = self.dict_app_excs['OutOfRange']
            KeyNotFound = self.dict_app_excs['KeyNotFound']
        self.AppExceptions = AppExceptions
    
    def setUp(self):
        self.load_eg_AppExceptions()
    
    def iter_app_excs(self):
        yield from zip(
            self.dict_app_excs.keys(),
            self.dict_app_excs.values(),
            self.AppExceptions
        )
    
    def test_args(self):
        for name, args, appexc in self.iter_app_excs():
            self.assertEqual(appexc.value, args.code)
            self.assertEqual(appexc.exc_type, args.exc_type)
            self.assertEqual(appexc.message, args.message)
    
    def test_lookup(self):
        for name, args, appexc in self.iter_app_excs():
            self.assertIs(appexc, self.AppExceptions[name])
            self.assertIs(appexc, self.AppExceptions(args.code))
    
    def test_throw(self):
        for name, args, appexc in self.iter_app_excs():
            with self.assertRaises(args.exc_type):
                appexc.throw()

if __name__ == '__main__':
    unittest.main(verbosity=2)

