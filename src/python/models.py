import numpy as np
from scipy import signal
from scipy import linalg

from iddata import IdData
from robustness import assert_positive, \
                       assert_nonnegative, \
                       assert_type

def arx(dat, orders, dt=1.0):
    # Validate inputs
    assert_type(dat, IdData)

    na, nb = orders
    assert_nonnegative(na)
    assert_nonnegative(nb)
    assert_positive(dt)

    # Extract data
    # TODO: Assume only one experiment for now
    (exp_samp, _, _, _) = dat.shape
    n_samp = exp_samp[0]
    y = dat.y[0]
    u = dat.u[0]

    # Compute maximum n
    max_n = max(na, nb)

    # Build auto regressive (AR) part of the PHI matrix
    phi_ar = _build_partial_phi_array(-1.0*y, na, max_n)

    # Build exogenous (X) part of the PHI matrix
    phi_x = _build_partial_phi_array(u, nb, max_n)

    # Build complete PHI matrix
    phi = np.hstack((phi_ar, phi_x))

    # Solve for theta
    theta = _theta_single_experiment(phi, y[max_n::])

    # Extract transfer function polynomial coefficients
    # TODO: Handle case where either na or nb are 0
    num = np.zeros(max_n)
    num[0:nb] = theta[na:na+nb]

    den = np.zeros(max_n+1)
    den[0:na+1] = np.hstack((1.0, theta[0:na]))

    return signal.TransferFunction(num, den, dt=dt)

def _theta_single_experiment(phi, y):
    theta, _, _, _ = linalg.lstsq(phi, y)
    return theta

def _build_partial_phi_array(arr, n, max_n):
    row_end = max_n-n-1
    if row_end < 0:
        row_end = None

    row = arr[max_n-1:row_end:-1]
    col = arr[max_n-1:-1]
    return linalg.toeplitz(col, row)
