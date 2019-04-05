import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

from iddata import IdData
from iddata_factory import FlightIdDataFactory as IdDataFactory
from models import arx
from control_utils import find_init_states, normalize
from iddata_factory import SmoothingModifier

"""
num_samp = 200
dt = 0.5
noise_scale = 4.0

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
"""

smoother = SmoothingModifier(5, 8)
factory = IdDataFactory(400)

for _ in range(5):
    dat = factory.create()
    #smooth_dat = IdData(smoother.apply(dat.y[0]), smoother.apply(dat.u[0]))
   
    # Find ARX model for original data
    m1 = arx(dat, orders=(40, 40))
    sys1 = m1.to_ss()
    x0 = find_init_states(sys1, dat.y[0], dat.u[0])
    t_out1, y_out1 = signal.dlsim(m1, dat.u[0], t=dat.time[0], x0=x0)

    """
    # Find ARX model for original data
    dat2 = IdData(smoother.apply(dat.y[0]), smoother.apply(dat.u[0]))
    m2 = arx(dat2, orders=(20, 20))
    sys2 = m2.to_ss()
    x0 = find_init_states(sys2, dat.y[0], dat.u[0])
    t_out2, y_out2 = signal.dlsim(m2, dat.u[0], t=dat.time[0], x0=x0)
    """

    plt.figure()
    plt.plot(dat.time[0], dat.y[0])
    plt.plot(t_out1, y_out1, 'r--')
    #plt.plot(t_out2, y_out2, 'g--')
plt.show()
