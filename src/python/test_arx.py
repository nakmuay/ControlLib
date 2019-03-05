import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

from iddata import iddata
from models import arx
from models import find_init_states

num_samp = 1000
dt = 0.1

t = dt*np.array(range(num_samp))
u = np.zeros((num_samp))
y = np.zeros((num_samp))
for i in range(num_samp):
    u[i] = np.sin(0.2*t[i] + 0.2) + np.cos(0.1*t[i]) + np.sin(0.5*t[i])
    y[i] = u[i] + 1.0*(np.random.rand() - 0.5)

    if i > 1:
        y[i] = y[i] + 0.6*y[i-1] + 0.25*y[i-2]

#u = np.array(range(10))
#y = 10*np.array(range(10))

dat = iddata(y, u)
m = arx(dat, 20, 20, dt)

print(m)

sys = m.to_ss()
x0 = find_init_states(sys, y, u)

#print("Model poles: {0}".format(m.poles))
t_out, y_out = signal.dlsim(m, u, t=t, x0=x0)

plt.plot(t, y)
plt.plot(t_out, y_out, 'r--')
plt.show()
