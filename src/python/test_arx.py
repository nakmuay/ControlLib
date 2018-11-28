import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

from iddata import iddata
from models import arx

num_samp = 200
f1 = 0.01
f2 = 0.04
t = np.array(range(num_samp))
u = np.sin(2*np.pi*f1*t)
y = u + 1/2*np.sin(2*np.pi*f2*t) + 1/10*np.random.rand(num_samp)

#u = np.array(range(10)) + 1
#y = u + 10

dat = iddata(y, u)

#dat.plot()

m = arx(dat, 10, 10)
m_ss = m.to_ss()

_, y_hat, _ = signal.dlsim(m_ss, u)
print(y_hat)

plt.plot(t, y)
plt.plot(t, y_hat, 'r--')
plt.show()
