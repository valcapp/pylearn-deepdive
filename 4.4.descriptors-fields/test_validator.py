import unittest
from parameterized import parameterized_class
# import pytest

from validator import RangeValidator, TypedRangeField, IntegerField, CharField

from functools import total_ordering
from dataclasses import dataclass
from math import sqrt
from numbers import Number

@total_ordering
@dataclass
class Pt2D:
    x: Number
    y: Number
    def __abs__(self):
        return sqrt(self.x**2 + self.y**2)
    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and abs(self) == abs(other)
        )
    def __lt__(self, other):
        return (
            isinstance(other, type(self))
            and abs(self) < abs(other)
        )

range_validator_params = (
    [(0,10,11)],
    [(5,20,0)],
    [('abc','defg','zzzz')],
    [(Pt2D(0,3),Pt2D(1,6.),Pt2D(10,10))],
    [(Pt2D(0,3),Pt2D(1,6.),Pt2D(0,0))],
)
class _TestRangeValidator():
    def setUp(self):
        # for some reason the test run a test case out of the
        # intended parameterized loop, so we feed the first
        # parametrization manually and run the loop sliced [1:]
        if not hasattr(self,'init'):
            self.init = range_validator_params[0][0]
        vtor = RangeValidator(*self.init[:2])
        class Obj:
            field = vtor
        self.vtor = vtor
        self.Obj = Obj
        
    def test_init(self):
        self.assertEqual(self.vtor.min, self.init[0])
        self.assertEqual(self.vtor.max, self.init[1])
    
    def test_set_name(self):
        self.assertEqual(self.vtor.name, 'field')
        self.assertEqual(self.Obj.field.name, 'field')

    def test_get(self):
        obj = self.Obj()
        self.assertEqual(self.Obj.field, self.vtor)
        self.assertEqual(obj.field, None)
    
    def test_set(self):
        obj = self.Obj()
        obj.field = self.init[0]
        self.assertEqual(obj.field, self.init[0])
        self.assertEqual(self.Obj.field, self.vtor)
        with self.assertRaises(ValueError):
            obj.field = self.init[2]
    
    def test_eval(self):
        for val in self.init:
            self.assertIs(self.vtor.eval(val), val)

@parameterized_class(['init'],range_validator_params[1:])
class TestRangeValidator(_TestRangeValidator, unittest.TestCase):
    """Tests RangeValidator descriptor"""

class _TestTypedRangeField(_TestRangeValidator):
    def test_init(self):
        super().test_init()
        with self.assertRaises(TypeError):
            TypedRangeField(self.init[0],self.init[3])
    def test_set(self):
        super().test_set()
        with self.assertRaises(TypeError):
            self.Obj().field = self.init[3]

integer_field_params = (
    [(0,10,15,'a')],
    [(0,100,-1,.3)],
)
class _TestIntegerField(_TestTypedRangeField):
    def setUp(self):
        # for some reason the test run a test case out of the
        # intended parameterized loop, so we feed the first
        # parametrization manually and run the loop sliced [1:]
        if not hasattr(self,'init'):
            self.init = integer_field_params[0][0]
        vtor = IntegerField(*self.init[:2])
        class Obj:
            field = vtor
        self.vtor = vtor
        self.Obj = Obj
@parameterized_class(['init'],integer_field_params[1:])
class TestIntegerField(_TestIntegerField, unittest.TestCase):
    """Tests IntegerField descriptor"""


char_field_params = (
    [('','12345','123456',.1)],
    [('foo','world','hi',tuple())],
)
class _TestCharField(_TestTypedRangeField):
    def setUp(self):
        if not hasattr(self,'init'):
            self.init = char_field_params[0][0]
        vtor = CharField(*map(len,self.init[:2]))
        class Obj:
            field = vtor
        self.vtor = vtor
        self.Obj = Obj
    def test_init(self):
        self.assertEqual(self.vtor.min, len(self.init[0]))
        self.assertEqual(self.vtor.max, len(self.init[1]))
        with self.assertRaises(TypeError):
            TypedRangeField(self.init[0],self.init[3])
    def test_eval(self):
        val = self.init[0]
        self.assertEqual(self.vtor.eval(val),len(val))
        
@parameterized_class(['init'],char_field_params[1:])
class TestCharField(_TestCharField, unittest.TestCase):
    """Tests IntegerField descriptor"""

if __name__ == '__main__':
    unittest.main()
    # loader = unittest.defaultTestLoader
    # suite = loader.loadTestsFromTestCase(TestRangeValidator)
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

# if __name__ == '__main__':
#     pytest.main([__file__])

