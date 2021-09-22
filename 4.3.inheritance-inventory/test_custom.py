import unittest
from custom import CPU, Storage, HDD, SSD

class TestCPU(unittest.TestCase):
    def test_init(self):
        expected_attrs = (
            'name','manufacturer',
            'cores', 'socket', 'power_watts',
            'total','allocated'
        )
        init_args = ('a','b',
            3, 'c', 94,
            3,2
        )
        rsc = CPU(*init_args)
        for attr, init_arg in zip(expected_attrs, init_args):
            self.assertEqual(
                getattr(rsc, attr),
                init_arg
            )
        self.assertEqual(rsc.category,'cpu')

class TestStorage(unittest.TestCase):
    def test_init(self):
        expected_attrs = (
            'name','manufacturer',
            'capacity_GB',
            'total','allocated'
        )
        init_args = (
            'a','b', 
            250,
            3,2
        )
        rsc = Storage(*init_args)
        for attr, init_arg in zip(expected_attrs, init_args):
            self.assertEqual(
                getattr(rsc, attr),
                init_arg
            )
        self.assertEqual(rsc.category,'storage')

class TestHDD(unittest.TestCase):
    def test_init(self):
        expected_attrs = (
            'name','manufacturer',
            'capacity_GB', 'size', 'rpm',
            'total','allocated'
        )
        init_args = (
            'a','b', 
            250, '12"', 2000,
            3,2
        )
        rsc = HDD(*init_args)
        for attr, init_arg in zip(expected_attrs, init_args):
            self.assertEqual(
                getattr(rsc, attr),
                init_arg
            )
        self.assertEqual(rsc.category,'hdd')

class TestSSD(unittest.TestCase):
    def test_init(self):
        expected_attrs = (
            'name','manufacturer',
            'capacity_GB', 'interface',
            'total','allocated'
        )
        init_args = (
            'a','b', 
            250, 'c',
            3,2
        )
        rsc = SSD(*init_args)
        for attr, init_arg in zip(expected_attrs, init_args):
            self.assertEqual(
                getattr(rsc, attr),
                init_arg
            )
        self.assertEqual(rsc.category,'ssd')
    