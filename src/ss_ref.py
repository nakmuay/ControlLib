import numpy as np
from matplotlib import pyplot as plt
from scipy import signal as sig

t = 0.1 * (np.array(range(500)) + 1)

u = np.sin(0.2 * t)
y = u**2


A = np.array([[2.0000092492084915, -1.0005452971553426],
              [1.0, 0.0]])

B = np.array([[1.0],
              [0.0]])

C = np.array([1.0229488355268767E-005, 0.0])

'''
tf = sig.TransferFunction([0, 4, 5, 6], [1, 2, 3, 0])
ss = tf.to_ss()
print(ss)
'''

print(A)
print(B)
print(C)

sys = sig.StateSpace(A, B, C, dt=0.1)

y_sim,y_sim,_ = sig.dlsim(sys, u)

plt.figure()
u_handle, = plt.plot(t, u, 'g', label="u")
y_handle, = plt.plot(t, y, 'b', label="true response")
y_sim_handle, = plt.plot(t, y_sim, 'r', label="true response")
plt.legend(handles=[u_handle, y_handle])

plt.draw()
plt.show()
