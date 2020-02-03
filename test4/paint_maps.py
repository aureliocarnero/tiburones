import astropy.io.fits as pf
import despyastro.wcsutil as wc
import healsparse as hs
import healpy as hp
import astropy.wcs as astrowcs
import os
import numpy as np
import skymap
from skymap import Skymap,McBrydeSkymap,OrthoSkymap
import matplotlib.pyplot as plt


dra = hp.read_map('mean_dra.fits')

ddec = hp.read_map('mean_ddec.fits')

dsep = hp.read_map('mean_dsep.fits')

draN = hp.read_map('mean_dra_new.fits')

ddecN = hp.read_map('mean_ddec_new.fits')

dsepN = hp.read_map('mean_dsep_new.fits')

#Old Dra
pix = []
paint = []
for j,val in enumerate(dra):
    if val!=hp.UNSEEN:
        pix.append(j)
        paint.append(val)

paint = np.array(paint)
pix = np.array(pix)

m = Skymap(projection='cass', lon_0=67., lat_0=-60.,celestial=False,
        llcrnrlon=56.68,urcrnrlon=77.46,
        llcrnrlat=-64.2,urcrnrlat=-55.40,
        parallels=False, meridians=False)

da=m.draw_hpxmap(paint,pix,nside=512,xsize=1000)

plt.colorbar()
plt.savefig('healpix_dra.png')
plt.close()

paintRA = paint.copy()

#New Dra

pix = []
paint = []
for j,val in enumerate(draN):
    if val!=hp.UNSEEN:
        pix.append(j)
        paint.append(val)

paint = np.array(paint)
pix = np.array(pix)

m = Skymap(projection='cass', lon_0=67., lat_0=-60.,celestial=False,
        llcrnrlon=56.68,urcrnrlon=77.46,
        llcrnrlat=-64.2,urcrnrlat=-55.40,
        parallels=False, meridians=False)

dd=m.draw_hpxmap(paint,pix,nside=512,xsize=1000)

paintRANEW = paint.copy()


plt.colorbar()
plt.savefig('healpix_dra_new.png')
plt.close()


plt.hist(paintRA,bins=100,label='Original',histtype='step',linewidth=2)
plt.hist(paintRANEW,bins=100,label='Corrected',histtype='step',linewidth=2)
plt.xlabel(r'$ra_{gaia}-ra_{VHS} [arcsec]$')
plt.legend()
plt.savefig('hist_ra.png')
plt.close()

#Old Ddec
pix = []
paint = []
for j,val in enumerate(ddec):
    if val!=hp.UNSEEN:
        pix.append(j)
        paint.append(val)

paint = np.array(paint)
pix = np.array(pix)

m = Skymap(projection='cass', lon_0=67., lat_0=-60.,celestial=False,
        llcrnrlon=56.68,urcrnrlon=77.46,
        llcrnrlat=-64.2,urcrnrlat=-55.40,
        parallels=False, meridians=False)

da=m.draw_hpxmap(paint,pix,nside=512,xsize=1000)

plt.colorbar()
plt.savefig('healpix_ddec.png')
plt.close()

paintDEC = paint.copy()

#New Ddec

pix = []
paint = []
for j,val in enumerate(ddecN):
    if val!=hp.UNSEEN:
        pix.append(j)
        paint.append(val)

paint = np.array(paint)
pix = np.array(pix)

m = Skymap(projection='cass', lon_0=67., lat_0=-60.,celestial=False,
        llcrnrlon=56.68,urcrnrlon=77.46,
        llcrnrlat=-64.2,urcrnrlat=-55.40,
        parallels=False, meridians=False)

dd=m.draw_hpxmap(paint,pix,nside=512,xsize=1000)

paintDECNEW = paint.copy()


plt.colorbar()
plt.savefig('healpix_ddec_new.png')
plt.close()


plt.hist(paintDEC,bins=100,label='Original',histtype='step',linewidth=2)
plt.hist(paintDECNEW,bins=100,label='Corrected',histtype='step',linewidth=2)
plt.xlabel(r'$dec_{gaia}-dec_{VHS}$ [arcsec]')
plt.legend()
plt.savefig('hist_dec.png')
plt.close()

#Old sep
pix = []
paint = []
for j,val in enumerate(dsep):
    if val!=hp.UNSEEN:
        pix.append(j)
        paint.append(val)

paint = np.array(paint)
pix = np.array(pix)

m = Skymap(projection='cass', lon_0=67., lat_0=-60.,celestial=False,
        llcrnrlon=56.68,urcrnrlon=77.46,
        llcrnrlat=-64.2,urcrnrlat=-55.40,
        parallels=False, meridians=False)

da=m.draw_hpxmap(paint,pix,nside=512,xsize=1000)

plt.colorbar()
plt.savefig('healpix_dsep.png')
plt.close()

paintSEP = paint.copy()

#New Ddec

pix = []
paint = []
for j,val in enumerate(dsepN):
    if val!=hp.UNSEEN:
        pix.append(j)
        paint.append(val)

paint = np.array(paint)
pix = np.array(pix)

m = Skymap(projection='cass', lon_0=67., lat_0=-60.,celestial=False,
        llcrnrlon=56.68,urcrnrlon=77.46,
        llcrnrlat=-64.2,urcrnrlat=-55.40,
        parallels=False, meridians=False)

dd=m.draw_hpxmap(paint,pix,nside=512,xsize=1000)

paintSEPNEW = paint.copy()


plt.colorbar()
plt.savefig('healpix_dsep_new.png')
plt.close()


plt.hist(paintDEC,bins=100,label='Original',histtype='step',linewidth=2)
plt.hist(paintDECNEW,bins=100,label='Corrected',histtype='step',linewidth=2)
plt.xlabel('Angular separation Gaia vs VHS [arcsec]')
plt.legend()
plt.savefig('hist_sep.png')
plt.close()

