def assert_type(arg, expected_type):
    actual_type = type(arg)
    if actual_type is not expected_type:
        msg = "Expected argument of type '{0}', got {1}".format(expected_type, actual_type)
        raise ValueError(msg)
