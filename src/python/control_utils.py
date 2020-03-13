import itertools
import random
import numpy as np
import scipy.linalg as linalg

def normalize(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

def arx_orders(na_orders, nb_orders, shuffle=False):
    products = itertools.product(na_orders, nb_orders)
    for p in products:
        yield p

def find_init_states(sys, y, u, horizon=float("inf")):
    # Extract system matrices
    A = sys.A
    B = sys.B
    C = sys.C
    D = sys.D

    if horizon > len(y):
        horizon = len(y)

    # Allocate ordinary least squares  matrices
    _, n_states = np.shape(C)
    lhs = np.zeros((horizon, 1))
    rhs = np.zeros((horizon, n_states))

    lhs[0] = y[0]
    rhs[0, :] = C
    for i in (n+1 for n in range(horizon-1)):
        CAprod = C
        CABSum = 0.0

        for j in reversed(range(i)):
            CABSum = CABSum + np.dot(CAprod, B*u[j])
            CAprod = np.dot(CAprod, A)

        lhs[i] = y[i] - CABSum - D*u[i]
        rhs[i, :] = CAprod

    # Solve for the initial states
    x0, _, _, _ = linalg.lstsq(rhs, lhs, cond=None)
    # TODO: Is it ok to flatten the result like this?
    return x0.reshape(1, x0.size)
