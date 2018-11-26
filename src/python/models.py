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

    print(y)
    print(u)

    # Compute maximum n
    max_n = max(na, nb)
    n_ident_samp = n_samp - max_n

    # Fill PHI matrix
    phi = allocate_array(n_ident_samp, na + nb)

    for row in phi:
        for i in range(na):
            row[i] = -y[max_n-i]


        print(row)

def allocate_array(n_rows, n_cols):
    return np.zeros(n_rows*n_cols).reshape(n_rows, n_cols)
