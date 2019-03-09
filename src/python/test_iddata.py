import numpy as np
from matplotlib import pyplot as plt
from iddata import IdData

num_samp = 10
t = np.array(range(num_samp))
in_dat = np.sin(t/2)
out_dat = in_dat**2
dat = IdData(out_dat, in_dat, expname="Experiment_0")

for i in range(1, 3):
    num_samp += 1
    t = np.array(range(num_samp))
    in_dat = np.sin(t/2 + i)
    out_dat_1 = in_dat + np.sin(t + np.pi/4) + np.sin(t + np.pi/3)
    out_dat_2 = np.array(out_dat_1) + 10

    name = "Experiment_{0}".format(i)
    dat.append(np.vstack((out_dat_1, out_dat_2)).T, in_dat, expname=name) 

print(dat.y)
print()

print(dat.u)
print()

print(dat.ts)
print()

print(dat.shape)
print()

dat.plot()
plt.show()
