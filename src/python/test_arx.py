import numpy as np
import matplotlib.pyplot as plt

from iddata import iddata
from models import arx

num_samp = 10
f1 = 0.01
f2 = 0.04
#t = np.array(range(num_samp))
#u = np.sin(2*np.pi*f1*t)
#y = u + 1/2*np.sin(2*np.pi*f2*t)

u = np.array(range(10)) + 1
y = u + 10

dat = iddata(y, u)

#dat.plot()

arx(dat, 2, 1)
