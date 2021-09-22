import unittest

from helpers import InsufficientResource
from resource import Resource

class TestResource(unittest.TestCase):
    def test_init(self):
        expected_attrs = ('name','manufacturer','total','allocated')
        init_args = ('a','b',3,2)
        rsc = Resource(*init_args)
        for attr, init_arg in zip(expected_attrs, init_args):
            self.assertEqual(
                getattr(rsc, attr),
                init_arg
            )
        self.assertEqual(rsc.category,'resource')
        self.assertEqual(rsc.available,1)
        with self.assertRaises(InsufficientResource):
            Resource('a','b',3,4)
        with self.assertRaises(TypeError):
            Resource('a','b',4,-4)
        with self.assertRaises(TypeError):
            Resource('a','b',-3,4)
        with self.assertRaises(TypeError):
            Resource('a','b',3.0,1)
    
    def test_str(self):
        self.assertEqual(
            str(Resource('a','b',3,2)),
            'a'
        )
    
    def test_repr(self):
        self.assertEqual(
            repr(Resource('a','b',3,2)),
            "Resource(name='a', manufacturer='b', total=3, allocated=2)"
        )
    
    def test_readonly(self):
        readonly_attrs =  ('name','manufacturer','total','allocated','available','category')
        rsc = Resource('a','b',3,2)
        for attr in readonly_attrs:
            with self.assertRaises(AttributeError):
                setattr(rsc, attr, 'hello')
    
    def test_claim(self):
        rsc = Resource('a','b',50,20)
        with self.assertRaises(InsufficientResource):
            rsc.claim(40)
        rsc.claim(20)
        self.assertEqual(rsc.total,50)
        self.assertEqual(rsc.allocated,40)
        self.assertEqual(rsc.available,10)
        
    def test_freeup(self):
        rsc = Resource('a','b',50,20)
        with self.assertRaises(InsufficientResource):
            rsc.freeup(30)
        rsc.freeup(10)
        self.assertEqual(rsc.total,50)
        self.assertEqual(rsc.allocated,10)
        self.assertEqual(rsc.available,40)
        
    def test_died(self):
        rsc = Resource('a','b',50,20)
        with self.assertRaises(InsufficientResource):
            rsc.died(40)
        rsc.died(20)
        self.assertEqual(rsc.total,30)
        self.assertEqual(rsc.allocated,20)
        self.assertEqual(rsc.available,10)
        
    def test_purchased(self):
        rsc = Resource('a','b',50,20)
        rsc.purchased(20)
        self.assertEqual(rsc.total,70)
        self.assertEqual(rsc.allocated,20)
        self.assertEqual(rsc.available,50)
    
    def test_expect_natural_methods(self):
        rsc = Resource('a','b',50,20)
        for method in ('claim','freeup','died','purchased'):
            bound_method = getattr(rsc,method)
            self.assertIsNone(bound_method(1))
            with self.assertRaises(TypeError):
                bound_method(.5)
            