import numpy as np
import scipy.signal as signal
import scipy.linalg as linalg

from iddata import iddata
from robustness import assert_nonnegative, \
                       assert_type

def arx(dat, na, nb, dt=1.0):

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
    num = theta[na::]
    den = np.hstack((np.array([1.0]), theta[0:na]))
    return signal.TransferFunction(num, den, dt=dt)

def _theta_single_experiment(phi, y):
    theta, _, _, _ = linalg.lstsq(phi, y)
    return theta

def _build_partial_phi_array(arr, n, max_n):
    col = arr[max_n-1::-1]
    row = arr[max_n-1:-1:]

    if (max_n-n > 0):
        col = arr[max_n-1:max(max_n-n-1, 0):-1]
        col = arr[max_n-1::-1]
    
    return linalg.toeplitz(row, 0.0*col)

def find_init_states(sys, y, u, horizon=None):
    # TODO: Fix bug causing large mismatch in initial state compared to reference signal
    A = sys.A
    B = sys.B
    C = sys.C
    D = sys.D

    if not horizon:
        horizon = len(y)

    _, n_states = np.shape(C)

    lhs = np.zeros((horizon, 1))
    rhs = np.zeros((horizon, n_states))

    for i in range(horizon):
        CAprod = C
        CABSum = 0.0

        for j in reversed(range(i)):
            CABSum = CABSum + np.dot(CAprod, B*u[j])
            CAprod = np.dot(CAprod, A)

        lhs[i] = y[i] - CABSum - D*u[i]
        rhs[i, :] = CAprod

    lhs[0] = y[0] - D*u[0]
    rhs[0, :] = C

    x0, _, _, _ = linalg.lstsq(lhs, rhs)
    return x0
