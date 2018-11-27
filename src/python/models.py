import numpy as np
import scipy.linalg as linalg

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

    # Build auto regressive (AR) part of the PHI matrix
    phi_ar = []
    if (max_n-na == 0):
        phi_ar = -linalg.toeplitz(y[max_n-1:-1:], y[max_n-1::-1])
    else:
        phi_ar = -linalg.toeplitz(y[max_n-1:-1:], y[max_n-1:max(max_n-na-1, 0):-1])

    # Build exogenous (X) part of the PHI matrix
    phi_x = []
    if (max_n-nb == 0):
        phi_x = linalg.toeplitz(u[max_n-1:-1:], u[max_n-1::-1])
    else:
        phi_x = linalg.toeplitz(u[max_n-1:-1:], u[max_n-1:max(max_n-nb-1, 0):-1])

    phi = np.hstack((phi_ar, phi_x))
    print("PHI:")
    print(phi)

    y_ident = y[max_n::]
    print("Y (identification)")
    print(y_ident)

    theta = _theta_single_experiment(phi, y_ident)
    print("Polynomial coefficients:")
    print(theta)

    # Extract transfer function polynomial coefficients
    den = np.hstack((np.array([1.0]), theta[0:na]))
    print("Denominator:")
    print(den)

    num = theta[na::]
    print("Numerator:")
    print(num)

def _theta_single_experiment(phi, y):
    theta, _, _, _ = linalg.lstsq(phi, y)
    return theta
