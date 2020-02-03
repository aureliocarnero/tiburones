import numpy as np
from astropy.coordinates import SkyCoord
import astropy.io.fits as pf
import healpy as hp
import scipy.optimize as so
from astropy import units as u

def delra(ra,dec):
    # RA transformation
    p0 = 0.38808
    p1 = 1.90683E-02
    p2 = 1.15439E-04

    gall, galb = cel2gal(ra,dec)
    ra_cor = 0.375 * (p0 + p1*galb + p2*galb**2)
    return (ra_cor/3600.)

def fit_ra(galb,p0,p1,p2):
    ra_cor = 0.375 * (p0 + p1*galb + p2*galb**2)
    return (ra_cor)#/3600.)

def fit_dec(alphaprime,p0,p1,p2):
    return 0.55 * (p0 + p1*alphaprime + p2*alphaprime**2)

def calalphaprime(ra,dec):
    ra_offset = 30.
    thetad = np.radians(45.)

    alphaprime = ra - 360*(ra > 180)
    alphaprime = alphaprime * np.cos(np.radians(dec)) - 30.

    deltaprime = dec + 30.

    r8temp1 = alphaprime*np.cos(thetad) - deltaprime*np.sin(thetad)
    r8temp2 = alphaprime*np.sin(thetad) + deltaprime*np.cos(thetad)

    alphaprime = r8temp1
    deltaprime = r8temp2

    return (alphaprime)

#This is a catalog with matching in TOPCAT between Gaia and VHS sources
sample_ = pf.open('/home/carnero/Documents/sharks/gaia/match_vhs_gaia.fits')[1].data

ra = sample_['ra2000']
dec = sample_['dec2000']

Dra = sample_['Dra']
Ddec = sample_['Ddec']
sep = sample_['Separation']

#Fit delta_ra

c = SkyCoord(ra, dec, frame='icrs', unit='deg')

gall = c.galactic.l
galb = np.array(c.galactic.b)
print(galb)

poptRa, pcovRa = so.curve_fit(fit_ra,galb,Dra)
print('parameters RA correction',poptRa)


alphaprime = calalphaprime(ra,dec)

poptDec, pcovDec = so.curve_fit(fit_dec,alphaprime,Ddec)
print('parameteris DEC correction',poptDec)

#Add corrections to VHS catalog before matching Gaia

vhs_ = pf.open('/home/carnero/Documents/sharks/vhs/catalog/vhs.fits')[1].data

raV = vhs_['ra2000']
decV = vhs_['dec2000']

cVHS = SkyCoord(raV, decV, frame='icrs', unit='deg')

galb = np.array(cVHS.galactic.b)
alphaprime = calalphaprime(raV,decV)

corr_raV = fit_ra(galb, poptRa[0], poptRa[1], poptRa[2])
corr_decV = fit_dec(alphaprime, poptDec[0], poptDec[1], poptDec[2])


cols = []
cols.append(pf.Column(name='corr_raV', format='D', array=corr_raV))
cols.append(pf.Column(name='corr_decV', format='D', array=corr_decV))
cols.append(pf.Column(name='ra2000', format='D', array=raV))
cols.append(pf.Column(name='dec2000', format='D', array=decV))
#cols.append(pf.Column(name='raNEW', format='D', array=raV+(corr_raV/3600.)))
#cols.append(pf.Column(name='decNEW', format='D', array=decV+(corr_decV/3600.)))


hdu = pf.BinTableHDU.from_columns(cols)

hdu.writeto('vhs_astrometric_corrected.fits',overwrite=True)
print('end of run')
