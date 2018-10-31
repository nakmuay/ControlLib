from robustness import assert_nonnegative

def arx(dat, na, nb):

    # Validate inputs
    #TODO: check input data is supported
    assert_nonnegative(na)   
    assert_nonnegative(nb)   
 
    # Extract data
    #y = dat.y
    #u = dat.u

    # Check maximum delay
    max_n = max(na, nb)
