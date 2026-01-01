import numpy as np

def assert_not_none(arg):
    if arg is None:
        raise ValueError("Expected argument to be not None")

def assert_type(arg, expected_type):
    actual_type = type(arg)
    if actual_type is not expected_type:
        msg = "Expected argument of type '{0}', got '{1}'".format(expected_type, actual_type)
        raise ValueError(msg)

def assert_array_like(arg):
    if not isinstance(arg, (list, np.ndarray)):
        msg = "Expected argument to be either list or numpy.ndarray"
        raise ValueError(msg)

def assert_nonnegative(arg):
    if not arg >= 0.0:
        msg = "Expected argument to be nonnegative, got '{0}'".format(arg)
        raise ValueError(msg)

def assert_positive(arg):
    if not arg > 0.0:
        msg = "Expected argument to be positive, got '{0}'".format(arg)
        raise ValueError(msg)
    
def assert_less_than(arg, upper_bound):
    if not arg < upper_bound:
        msg = "Expected argument to be less than '{0}', got '{1}'".format(upper_bound, arg)
        raise ValueError(msg)
    
def assert_equal(first, second):
       if not first == second:
        msg = "Expected argument to be equal, got '{0}' and '{1}'".format(first, second)
        raise ValueError(msg) 