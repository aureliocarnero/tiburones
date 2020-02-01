# Test1

In this example I show how to transform a VHS weight image into a healpix map of different resolutions.

Ideally, this can also be done with ANCILLARY.MASK files, creating a coverage mask.


Having the variations along the footprint in Healpix format is very convenient for several applications:

- Make sources density maps, weighted by the effective area observed, which can be use, for example, to estimate galaxy-galaxy correlation functions and galaxy-weight correlation function.

- Study density versus footprint inhomogeneities

Dependencies:

- astropy https://www.astropy.org/
- skymap https://github.com/kadrlica/skymap
- despyastro https://github.com/DarkEnergySurvey/despyastro
- healsparse https://github.com/lsstdesc/healsparse
- healpy https://healpy.readthedocs.io/en/latest/
- numpy https://numpy.org/
- matplotlib https://matplotlib.org/

Test images:

Download an image and associated weight image from ESO phase 3 portal. For example, from here: http://eso.org/rm/publicAccess#/dataReleases
 - Go to VHS DR4
 - Go to http://archive.eso.org/wdb/wdb/adp/phase3_main/query and select, for example, all products with filter = Ks. You can additionally select RA,DEC coordinates.
 - Select any SCIENCE.IMAGE
 - Select Instant download
 - Select All
 - Download Selected


