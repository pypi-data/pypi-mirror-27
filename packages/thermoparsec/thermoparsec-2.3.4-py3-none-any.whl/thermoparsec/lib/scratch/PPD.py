from numpy import sqrt, pi, exp,loadtxt
from lmfit import Model
import numpy as np
#import matplotlib.pyplot as plt

def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(sqrt(2*pi)*wid)) * exp(-(x-cen)**2 /(2*wid**2))

def PPD(trace,w):
    x = []
    y = []
    for i in range(len(trace)):
        x.append(trace[i].RT)
        y.append(trace[i].Intensity)
    x = np.asarray(x)
    y = np.asarray(y)
    amp = np.median(y)
    cent = np.median(x)
    gmodel = Model(gaussian)

    return gmodel.fit(y, x=x, amp=amp, cen=cent, wid=w)

