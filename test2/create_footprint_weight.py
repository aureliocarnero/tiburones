import multiprocessing as mp
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

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def worker(image,return_dict,procnum):
#Read image header and get coordinates of the image


    print(i,'working with image',image)
    hdr=pf.open(image)
    w=astrowcs.WCS(hdr[1].header)
    corners_image=w.calc_footprint(center=False)
    corners_pixels=w.calc_footprint(center=True)
    nx = hdr[1].header['naxis1']
    ny = hdr[1].header['naxis2']

    coords1 = corners_image[0]
    coords2 = corners_image[1]
    coords3 = corners_image[2]
    coords4 = corners_image[3]
#Read image data
    image_data = pf.getdata(image)

#Define healsparse polygon within the image
    ra = [coords1[0],coords4[0],coords3[0],coords2[0]]
    dec = [coords1[1],coords4[1],coords3[1],coords2[1]]
    raC = (np.max(ra)+np.min(ra))/2.
    decC = (np.max(dec)+np.min(dec))/2.

    nside = 2**17
    poly = hs.Polygon(
        ra=ra,
        dec=dec,
        value=1)
    smap = poly.get_map(nside=nside, dtype=np.int16)
    a = smap.validPixels

    b=hp.nest2ring(nside,a)
#a are pixels in NEST, b in RING
#Get center coordinates of each pixel
    raF,decF =hp.pix2ang(nside,a,lonlat=True,nest=True)

#Get nx, ny in image from healsparse pixels
    myhdr=hdr[1].header
    wcs = wc.WCS(myhdr)
    xn,yn = wcs.sky2image(raF,decF)
#Get associated weight values
    values = []
    for x,y in zip(xn,yn):

        values.append(image_data[int(y-1),int(x-1)])

    values = np.array(values)
#Define healsparse map
    hsp_map_2 = hs.HealSparseMap.makeEmpty(512, nside, dtype=np.int16)

    hsp_map_2.updateValues(a, values)

#Degrade to nside=4096
    low_res_hsp = hsp_map_2.degrade(4096)

    j = low_res_hsp.validPixels

    test_values_2 = low_res_hsp.getValuePixel(j)

#Uncomment if you want in RING format
    #k=hp.nest2ring(4096,j)

    #hp_aux = np.zeros(hp.nside2npix(4096))+hp.UNSEEN
    #hp_aux[j] = test_values_2

    hdr.close()

    return_dict[procnum] = np.array([j,test_values_2]).transpose()
    

if __name__ == '__main__':
#Change accordingly to your path
    path='/home/carnero/Documents/sharks/vhs/images'

    w_images = []
    for files in os.listdir(path):
        if files.endswith('.fits.fz'):
            w_images.append(os.path.join(path,files))
    dim=len(w_images)
    print('Number of images to process = ',dim)

#In my case, divide in chunks of size=2 
    eso = list(chunks(w_images,2))
    print (eso)
    print(len(eso)) 
    mymap = []
    for jj,esa in enumerate(eso):
        manager = mp.Manager()
        return_dict = manager.dict()
        jobs = []
        for i in range(2):
            p = mp.Process(target=worker, args=(esa[i],return_dict,i))
            jobs.append(p)
            p.start()
        for proc in jobs:
            proc.join()
        if jj==0:
            print(return_dict)
        mymap.append(return_dict)

#I created a list of dictionaries. Now loop in each image to create a single healpix map. Next should be improved, it is hardwire to 2 process in parallel

    pixels_map,values_map = [],[]
    for inside in mymap:
            
        vals_0 = inside[0]
        vals_1 = inside[1]
        for val in vals_0:
            if val[1]!=0.:
                pixels_map.append(val[0])
                values_map.append(val[1])
        for val in vals_1:
            if val[1]!=0.:
                pixels_map.append(val[0])
                values_map.append(val[1])

    pixels_map = np.array(pixels_map)
    values_map = np.array(values_map)
    print(len(pixels_map))
    print(len(np.unique(pixels_map)))

#Fill healpix map at NSIDE=4096
    hp_aux = np.zeros(hp.nside2npix(4096))+hp.UNSEEN

    for pp,vv in zip(pixels_map,values_map):
        if hp_aux[int(pp)]==0. or hp_aux[int(pp)]==hp.UNSEEN:
            hp_aux[int(pp)]=vv
    hp.write_map('combined_map.fits', hp.ma(hp_aux), overwrite=True, nest=True, fits_IDL=False, partial=True)

#Make plot of the healpix map
    upix, uval = [],[]
    for jj,vv in enumerate(hp_aux):
        if vv!=hp.UNSEEN:
            upix.append(jj)
            uval.append(vv)

    upix = np.array(upix)
    uval = np.array(uval)

    k=hp.nest2ring(4096,upix)

    m = Skymap(projection='cass', lon_0=67., lat_0=-60.,celestial=False,
        llcrnrlon=56.68,urcrnrlon=77.46,
        llcrnrlat=-64.2,urcrnrlat=-55.40,
        parallels=False, meridians=False)
    
    m.draw_hpxmap(uval,k,nside=4096,xsize=1000)
    plt.savefig('healpix_imageLow.png')

