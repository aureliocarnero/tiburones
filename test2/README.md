# Test2

In this example we extend test1 to a large area, creating a VHS weight healpix map from individual images. We use multiprocessing to parallelize the image mask creation.

Use create_footprint_weight.py for this first step

As a second step, we use this information to calculate the dependence between source density as a function of image weight. It uses a private DES python library.

Use dens_vs_weight_example.py


Dependencies (python 3.):

- astropy https://www.astropy.org/
- skymap https://github.com/kadrlica/skymap
- despyastro https://github.com/DarkEnergySurvey/despyastro
- healsparse https://github.com/lsstdesc/healsparse
- healpy https://healpy.readthedocs.io/en/latest/
- numpy https://numpy.org/
- matplotlib https://matplotlib.org/
- multiprocessing https://docs.python.org/3/library/multiprocessing.html
- lsssys [DES private]



Images:

Download images, catalogs and associated weight images from ESO phase 3 portal. Images comes both from VHS DR4. and VHS DR4.1.
We select an area in the limits RA between 56.68 and 77.46 and DEC between -64.2 and -55.40.


