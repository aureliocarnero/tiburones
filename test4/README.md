# Test4

Astrometric corrections.

We compare the astrometric solution of VHS versus Gaia, and correct possible inhomogeneities.

In an area selected in the limits RA between 56.68 and 77.46 and DEC between -64.2 and -55.40.

1) Match original VHS catalog to Gaia using original coordinates from VHS. Calculate Dra and Ddec in arcseconds
2) Calculate astrometric corrections to apply to VHS to improve astrometry with respect to Gaia (run fit_d.py)
3) Correct original VHS coordinates
4) Match new VHS coordinates to Gaia and calculate Dra and Ddec in arcseconds
5) Create healpix maps of Dra, Ddec, Separation, both for the original VHS coordinates and the new corrected ones (run create_maps.py)
6) Paint the healpix maps for all Dra, Ddec and separations, as well as histogram comparing boths (run paint_maps.py)



Dependencies (python 3.):

- astropy https://www.astropy.org/
- skymap https://github.com/kadrlica/skymap
- scipy 
- healsparse https://github.com/lsstdesc/healsparse
- healpy https://healpy.readthedocs.io/en/latest/
- numpy https://numpy.org/
- matplotlib https://matplotlib.org/


Data:

Download Gaia and VHS data. We select an area in the limits RA between 56.68 and 77.46 and DEC between -64.2 and -55.40.


