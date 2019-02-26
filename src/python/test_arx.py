import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

from iddata import iddata
from models import arx
from models import find_init_states

num_samp = 1000
f1 = 0.01
f2 = 0.06
t = np.array(range(num_samp))
u = np.sin(2*np.pi*f1*t)
y = u + 1/4*np.sin(2*np.pi*f2*t) + 1/10*np.random.rand(num_samp)

dat = iddata(y, u)
m = arx(dat, 10, 10)

x0 = find_init_states(m.to_ss(), y, u)
print(x0)

#print("Model poles: {0}".format(m.poles))
t_out, y_out = signal.dlsim(m, u, t=t, x0=x0)

plt.plot(t, y)
plt.plot(t_out, y_out, 'r--')
plt.show()
