import numpy as np
from iddata import iddata

num_samp = 100
t = np.array(range(num_samp))
in_dat = np.sin(t/2)
out_dat = in_dat**2
dat = iddata(out_dat, in_dat, expname="Experiment_0")

for i in range(1, 3):
    num_samp += 1
    t = np.array(range(num_samp))
    in_dat = np.sin(t/2 + i)
    out_dat = in_dat + np.sin(t + np.pi/4) + np.sin(t + np.pi/3)

    name = "Experiment_{0}".format(i)
    dat.append(out_dat, in_dat, expname=name) 

print(dat.y)
print(dat.u)
print(dat.ts)

print(dat.shape)

dat.plot()

