import numpy as np
from matplotlib import pyplot as plt
from iddata import IdData

num_samp = 10
t = np.array(range(num_samp))
in_dat = np.sin(t/2)
out_dat = in_dat**2
dat = IdData(out_dat, in_dat, expname="Experiment_0")

for i in range(1, 3):
    t = np.arange(num_samp)
    in_dat1 = np.sin(t/2 + i)
    out_dat1 = in_dat1 + np.sin(t + np.pi/4) + np.sin(t + np.pi/3)

    in_dat2 = np.sin(t/3 + i)
    out_dat2 = in_dat2 + np.sin(t + np.pi/5) + np.sin(t + np.pi/4)

    name = "Experiment_{0}".format(i)
    out_dat = np.vstack((out_dat1, out_dat2))
    in_dat = np.vstack((in_dat1, in_dat2))
    dat.append(out_dat, in_dat, expname=name)
    
dat.plot()
plt.show()
