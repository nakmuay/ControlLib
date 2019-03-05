import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

from iddata import iddata
from models import arx
from control_utils import find_init_states, normalize


num_samp = 200
dt = 0.5
noise_scale = 2.0

t = dt*np.array(range(num_samp))
u = np.zeros((num_samp))
y = np.zeros((num_samp))
for i in range(num_samp):
    u[i] = np.sin(0.2*t[i] + 0.2) + np.cos(0.1*t[i]) + np.sin(0.5*t[i])
    y[i] = u[i] + noise_scale*(np.random.rand() - 0.5)

    if i > 1:
        y[i] = y[i] + 0.6*y[i-1] + 0.25*y[i-2] + u[i] + noise_scale*(np.random.rand() - 0.5)

y = y + 10.0

u = normalize(u)
y = normalize(y)

dat = iddata(y, u)
m = arx(dat, 20, 20, dt)

sys = m.to_ss()
print("Model poles: {0}".format(m.poles))
print("B: {0}".format(sys.B))

x0 = find_init_states(sys, y, u)
print("Initial states: {0}".format(x0))

t_out, y_out = signal.dlsim(m, u, t=t, x0=x0)

plt.plot(t, y)
plt.plot(t_out, y_out, 'r--')
plt.show()
