from iddata import iddata
from robustness import assert_nonnegative, \
                       assert_type

def arx(dat, na, nb):

    # Validate inputs
    #TODO: check input data is supported
    assert_type(dat, iddata)
    assert_nonnegative(na)   
    assert_nonnegative(nb)   
 
    # Extract data
    # TODO: Assume only one experiment for now
    (exp_samp, _, _, _) = dat.shape
    n_samp = exp_samp[0]

    y = dat.y[0]
    u = dat.u[0]

    # Check maximum delay
    max_n = max(na, nb)

    print(y)

