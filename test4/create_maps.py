import numpy as np
from astropy.coordinates import SkyCoord
import astropy.io.fits as pf
import healpy as hp


nside=512

def gen_fast_map(ip_, nside=512):
    npixel  = hp.nside2npix(nside)
    map_ = np.bincount(ip_,minlength=npixel)
    return map_

#Old correction
sample_ = pf.open('/home/carnero/Documents/sharks/gaia/match_vhs_gaia.fits')[1].data

ra = sample_['ra2000']
dec = sample_['dec2000']

Dra = sample_['Dra']
Ddec = sample_['Ddec']
sep = sample_['Separation']


pix_id = hp.ang2pix(nside, ra, dec, lonlat=True, nest=True)
map_ = gen_fast_map(pix_id, nside=nside)

empty_map = np.array([hp.UNSEEN]*len(map_))

for j,val in enumerate(map_):
        if val!= 0:
                empty_map[j]=val

filled_pixels = []
for j,val in enumerate(empty_map):
    if val!=hp.UNSEEN:
        filled_pixels.append(j)

filled_pixels = np.array(filled_pixels)

mean_dra, mean_ddec, mean_sep = [],[],[]

for pix in filled_pixels:
    mask = (pix_id==pix)
    mean_dra.append(np.mean(Dra[mask]))
    mean_ddec.append(np.mean(Ddec[mask]))
    mean_sep.append(np.mean(sep[mask]))

map_dra = np.array([hp.UNSEEN]*len(map_))
map_ddec = np.array([hp.UNSEEN]*len(map_))
map_sep = np.array([hp.UNSEEN]*len(map_))

for jj,pix in enumerate(filled_pixels):
    map_dra[pix]=mean_dra[jj]
    map_ddec[pix]=mean_ddec[jj]
    map_sep[pix]=mean_sep[jj]

hp.write_map('mean_dra.fits',hp.ma(map_dra),nest=True,fits_IDL=False,partial=True,overwrite=True)
hp.write_map('mean_ddec.fits',hp.ma(map_ddec),nest=True,fits_IDL=False,partial=True,overwrite=True)
hp.write_map('mean_dsep.fits',hp.ma(map_sep),nest=True,fits_IDL=False,partial=True,overwrite=True)

#print(results)


#NEw correction
sample_ = pf.open('match_vhs_gaia_new.fits')[1].data

ra = sample_['raNEW']
dec = sample_['decNEW']

Dra = sample_['Dra_new']
Ddec = sample_['Ddec_new']
sep = sample_['Separation']


pix_id = hp.ang2pix(nside, ra, dec, lonlat=True, nest=True)
map_ = gen_fast_map(pix_id, nside=nside)

empty_map = np.array([hp.UNSEEN]*len(map_))

for j,val in enumerate(map_):
        if val!= 0:
                empty_map[j]=val

filled_pixels = []
for j,val in enumerate(empty_map):
    if val!=hp.UNSEEN:
        filled_pixels.append(j)

filled_pixels = np.array(filled_pixels)

mean_dra, mean_ddec, mean_sep = [],[],[]

for pix in filled_pixels:
    mask = (pix_id==pix)
    mean_dra.append(np.mean(Dra[mask]))
    mean_ddec.append(np.mean(Ddec[mask]))
    mean_sep.append(np.mean(sep[mask]))

map_dra = np.array([hp.UNSEEN]*len(map_))
map_ddec = np.array([hp.UNSEEN]*len(map_))
map_sep = np.array([hp.UNSEEN]*len(map_))

for jj,pix in enumerate(filled_pixels):
    map_dra[pix]=mean_dra[jj]
    map_ddec[pix]=mean_ddec[jj]
    map_sep[pix]=mean_sep[jj]

hp.write_map('mean_dra_new.fits',hp.ma(map_dra),nest=True,fits_IDL=False,partial=True,overwrite=True)
hp.write_map('mean_ddec_new.fits',hp.ma(map_ddec),nest=True,fits_IDL=False,partial=True,overwrite=True)
hp.write_map('mean_dsep_new.fits',hp.ma(map_sep),nest=True,fits_IDL=False,partial=True,overwrite=True)


