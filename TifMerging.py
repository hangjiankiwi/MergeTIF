# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:23:46 2019

@author: Hangjian
"""
import rasterio 
from rasterio.merge import merge
import glob
import os

#Define the function for merging all the individual rasters
def mergingTIF(path,ftype,outfile):
    #Define the path where all the subtifs located
    alltif=glob.glob(os.path.join(path,'*.%s'%ftype))
    #Preallocate the list
    bigtif=[]
    #Read in the individual tif
    print('Start reading the individual tif file...')
    n=1
    for tif in alltif:
        src=rasterio.open(tif)
        bigtif.append(src)
        print(tif)
        n=n+1
        print(n)
    #Conduct merging
    mosaic, out_trans = merge(bigtif)
    #Extracting the original meta data
    print('Update the META data...')
    outmeta=src.meta.copy()
    outmeta.update({'driver':'GTiff','height':mosaic.shape[1],'width':mosaic.shape[2],'transform':out_trans})
    
    print('Write the file...')
    os.makedirs(path+'\\Merged')
    outpath=path+'\\Merged\%s.tif'%outfile
    with rasterio.open(outpath,'w',**outmeta) as dest:
        dest.write(mosaic)

#%%Function execution
#Define the path for sub tif files
path=r'\Inputs'
#Define the name for the merged file
outfile='AKL_satellite'
#Define the subfile type
ftype='jpg'    #tif/jpg
#Run merging
mergingTIF(path,ftype,outfile)
