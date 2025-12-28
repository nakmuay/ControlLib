import itertools
import numpy as np
from scipy import linalg

def normalize(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

def arx_orders(na_orders, nb_orders, shuffle=False):
    products = itertools.product(na_orders, nb_orders)
    yield from products

def find_init_states(sys, y, u, horizon=float("inf")):
    # handle max horizon
    horizon = min(horizon, len(y))

    # Allocate ordinary least squares  matrices
    _, n_states = np.shape(sys.C)
    lhs = np.zeros((horizon, 1))
    rhs = np.zeros((horizon, n_states))

    lhs[0] = y[0]
    rhs[0, :] = sys.C
    for i in (n+1 for n in range(horizon-1)):
        CAprod = sys.C
        CABSum = 0.0

        for j in reversed(range(i)):
            CABSum = CABSum + np.dot(CAprod, sys.B*u[j])
            CAprod = np.dot(CAprod, sys.A)

        lhs[i] = y[i] - CABSum - sys.D*u[i]
        rhs[i, :] = CAprod

    # Solve for the initial states
    x0, _, _, _ = linalg.lstsq(rhs, lhs, cond=None)
    # TODO: Is it ok to flatten the result like this?
    return x0.reshape(1, x0.size)
