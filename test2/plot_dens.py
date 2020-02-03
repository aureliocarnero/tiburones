import matplotlib
import numpy as np 
import matplotlib.pyplot as plt 
import os
import sys

x,y,err_jk = np.loadtxt('dens_vs_weight.txt',unpack=True)

plt.errorbar(x,y,err_jk, fmt='.', color='k')
#plt.errorbar(x,y/ngal_mean,err_jk/ngal_mean, fmt='.', color='k')
#plt.axhline(1, color='g', ls='--')
plt.xlabel('VHS image weight')
#plt.ylabel(r'$N_{\rm gal}/ \langle N_{\rm gal} \rangle $')
plt.ylabel(r'$Density$')
#title='{0} < z < {1}'.format(zmin,zmax)
#plt.title(title)
plt.grid()
imagename='dens_vs_weight.png'
plt.savefig(imagename)
plt.close()


