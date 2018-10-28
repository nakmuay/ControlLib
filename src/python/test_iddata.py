import numpy as np
from iddata import iddata

num_samp = 10
in_dat = np.array(range(num_samp))
out_dat = in_dat**2

dat = iddata(out_dat, in_dat, expname="Experiment_1") 
dat2 = iddata(np.array(range(num_samp)), in_dat, ts=1, expname="Experiment_1") 

in_dat[0] = 1000

dat.append(out_dat, in_dat, expname="Experiment_2") 
dat.append(out_dat, in_dat) 


dat.plot()

