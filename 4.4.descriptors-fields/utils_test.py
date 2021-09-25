from types import MappingProxyType
from parameterized import parameterized_class
import unittest
from typing import Iterable
import functools

def register_testcase(globs:MappingProxyType, original_class:type, params:Iterable=None)->type:
    """This is to be able to write classes that looks like TestCase classes
    but can inherit test methods between them, and then only at the end call
    this function, at the end, to register them as TestCases"""
    class_name = original_class.__name__.strip('_')
    if not class_name.startswith('Test'):
        class_name = 'Test'+class_name
    testcase_class = type(
        class_name,
        (original_class, unittest.TestCase),
        {}
    )
    if params is not None:
        testcase_class = parameterized_class(*params)(testcase_class)
    globs[class_name] = testcase_class

def testcased(original_class:type)->type:
    """Decorator to register class as unittest.TestCase"""
    register_testcase(original_class)
    return original_class

def parameterized_testcase(*params)->type:
    """Decorator factory to register class as parameterized unittest.TestCase"""
    @functools.wraps
    def testcased(original_class:type)->type:
        register_testcase(original_class, params)
        return original_class
    return testcased