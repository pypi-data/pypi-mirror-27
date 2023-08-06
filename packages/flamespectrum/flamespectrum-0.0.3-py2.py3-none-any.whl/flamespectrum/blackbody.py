# -*- coding: utf-8 -*-
import numpy as np
import math
## 太阳
h=6.62606957e-34      #普朗克常数
k=1.3806e-23
c=2.99792458e8

def calculate(T,alpha=1,wavestart=0.5,wavestop=6):

    wave=np.linspace(wavestart/1e6,wavestop/1e6,1000)

    L=2*np.pi*h*c**2/(wave**5)/(np.exp(h*c/(wave*k*T))-1)

    rad = alpha * L / np.pi / 1e10 ##单位 W / cm2 sr um

    return wave*1e6,rad



