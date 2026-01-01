from scipy import signal
from matplotlib import pyplot as plt

from iddata_factory import FlightIdDataFactory as IdDataFactory
from models import arx
from control_utils import find_init_states
from signal_modifier import SmoothingModifier

smoother = SmoothingModifier(3, 10)
factory = IdDataFactory(500)

for _ in range(1):
    dat = factory.create()

    # Find ARX model for original data
    m1 = arx(dat, orders=(50, 10))
    sys1 = m1.to_ss()
    x0 = find_init_states(sys1, dat.y[0], dat.u[0])
    t_out1, y_out1 = signal.dlsim(m1, dat.u[0], t=dat.time[0], x0=x0)

    # Find ARX model for smoothed data
    smooth_dat = smoother.apply(dat)
    m2 = arx(smooth_dat, orders=(20, 20))
    sys2 = m2.to_ss()
    x0 = find_init_states(sys2, smooth_dat.y[0], smooth_dat.u[0])
    t_out2, y_out2 = signal.dlsim(m2, smooth_dat.u[0], t=smooth_dat.time[0], x0=x0)

    plt.figure()
    plt.plot(dat.time[0], dat.y[0])
    plt.plot(t_out1, y_out1, 'r--')

    """
    plt.figure()
    plt.plot(smooth_dat.time[0], smooth_dat.y[0])
    plt.plot(t_out2, y_out2, 'g--')
    """

plt.show()
