import matplotlib
import lsssys
import numpy as np 
import matplotlib.pyplot as plt 
import os
import sys
import time
import healpy as hp
import healpix_util as hu
import errno
import astropy.io.fits as pf

sysmapM = 'combined_map.fits'
maskmap = 'mask_map.fits'


catfile = '/home/carnero/Documents/sharks/vhs/catalog/vhs.fits' 


maskpixname = 'PIXEL'
fracpixname = 'T'

nside = 4096
label = 'vhs_weight'

mainoutdir = './'







use_equalarea_bins = True

nbins1d = 20

####magnitude within catalog
zcol = 'LAMBDA'
errzcol = 'LAMBDA'
magcol = 'KSAPERMAG3'
idcol = 'KSAPERMAG3ERR'


############# outputs
savechi2=False
saveplot=True
saveplotdata=False

############# Error bars (JK, bootstrap or mocks)

kmeans0=False
usemaskforcenters=True
#jkpix=100
jkpix=None
tol=1.0e-4
samejkregions=False
#nboots=100
nboots = None
bootssize=1.0
mockerrorbars = True


mask = lsssys.mask(maskmap, ZMAXcol = None, maskpixname=maskpixname, fracpixname=fracpixname, input_order='NEST')

sysmap = lsssys.Map()
sysmap.sysmap(sysmapM)
sysmap.addmask(mask  = mask.mask,  fracdet=mask.fracdet)
assert (sysmap.mask==mask.mask).all()==True
assert (sysmap.fracdet==mask.fracdet).all()==True

sample_ = pf.open(catfile)[1].data

ra = sample_['ra2000']
dec = sample_['dec2000']

galmap = lsssys.cat2galmap(ra,dec, mask, weight=None, nside = 4096)

sysmap.addmask(galmap.mask)
galmap.addmask(sysmap.mask)
assert (galmap.mask == sysmap.mask).all() == True
assert (galmap.fracdet ==  sysmap.fracdet).all() == True
	
if use_equalarea_bins==True:
    binedges = lsssys.equal_area_bin_edges(sysmap,nbins=nbins1d)
    print( 'Using binedges. nbins and trim values will be ignored')
else:
    binedges = None
trim = 0.01
	
x,y,err_jk, ngal_mean = lsssys.binned_xyerr(sysmap, galmap, nbins = nbins1d, trim = trim, binedges = binedges, overmean=False, returnmean=True, nboots=nboots, bootssize=bootssize, jkpix=jkpix, removezeros=False)

np.savetxt('dens_vs_weight.txt',np.array([x,y,err_jk]).transpose())

