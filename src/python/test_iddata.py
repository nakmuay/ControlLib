import numpy as np
from iddata import iddata

num_samp = 10
in_dat = np.array(range(num_samp))
out_dat = in_dat**2

dat = iddata(out_dat, in_dat, expname="Experiment_1") 

in_dat[0] = 1000

dat.append(out_dat, in_dat, expname="Experiment_2") 
dat.append(out_dat, in_dat) 

print(dat.y)
print(dat.u)
print(dat.ts)

dat.plot()

