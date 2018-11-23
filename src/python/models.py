import numpy as np

from iddata import iddata
from robustness import assert_nonnegative, \
                       assert_type

def arx(dat, na, nb):

    # Validate inputs
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

    # Fill PHI matrix
    phi = allocate_array(n_samp - 1, na + nb)

    for row in phi:
        row[0:na] = 1 
        row[na:na + nb] = 2

        print(row)

def allocate_array(n_rows, n_cols):
    return np.zeros(n_rows*n_cols).reshape(n_rows, n_cols)
