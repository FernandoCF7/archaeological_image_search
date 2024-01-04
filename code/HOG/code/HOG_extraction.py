"""
Created on Thu Jan  9 19:42:39 2020

@author: fernando
"""

#-----------------------------------------------------------------------------#
#clear stored variables
from IPython import get_ipython
get_ipython().magic('reset -sf')
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
import os
import sys
import pandas as pd
import h5py
import cv2 as cv

currentPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append("{0}/../../HOG/code".format(currentPath))
from hog import HOG
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Walk into ../../variables/ROI/images directory
for dir_path, dir_names, image_names in os.walk( os.path.join("..", "..", "variables", "ROI", "images") ):
    
    #-------------------------------------------------------------------------#
    #Create (if no exist) the directories to store the HOGvectorsPerImg
    
    #Set HOG directory name as current dir_path
    fileHOGpath = os.path.join("..", "..", "variables", "HOG", "{0}".format(dir_path[27:]))
    
    #make HOG directory if doesn't exist
    if os.path.isdir(fileHOGpath) == False: os.mkdir(fileHOGpath)
    #-------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------#
    #Make (if doesn't exist) file HOGallImgs.hdf5 --> all HOG imgs vects
    with h5py.File(os.path.join("..", "..", "variables", "HOG", "HOGallImgs.hdf5"), "a") as f:
        pass
        #f.create_dataset("allHOGvectors",(0,36),maxshape=(None,36))
    
    #Make (if doesn't exist) file HOGshapeAllImgs.hdf5-->stores [M,N] HOG shape
    with h5py.File(os.path.join("..", "..", "variables", "HOG", "HOGshapeAllImgs.hdf5"), "a") as f:
        pass
    #-------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------#
    #From ROI directory --> get the list of images
    HOGfilesList = next( os.walk(fileHOGpath) )[2]
    ROIfilesList = next( os.walk(dir_path) )[2]#fileROIpath-->dir_path

    #ROIfilesList --> discard those images that have not a valid image extension
    tmp = []
    for image_name in ROIfilesList:
        image_name_splited = image_name.split(".")
        if len(image_name_splited) > 1 and image_name_splited[-1].lower() in ["jpg", "jpeg", "png", "gif", "tif", "tiff", "bmp", "webp", "pbm", "pgm", "ppm", "exr"]:
            tmp.append(image_name)
        else:
            print("Warning: file {}/{} has not a valid image extension".format(dir_path, image_name))
    ROIfilesList = tmp 

    #ROIfilesList --> exclude those images that already have HOG vectors
    
    #Delete the .extention of the list names; _WE-->without extention
    HOGfilesList_WE = [os.path.splitext(c1)[0] for c1 in HOGfilesList]
    ROIfilesList_WE = [os.path.splitext(c1)[0] for c1 in ROIfilesList]    
    
    #Convert HOGfilesList_WE and ROIfilesList_WE in pd.Series
    HOGfilesList_WE = pd.Series(HOGfilesList_WE)
    ROIfilesList_WE = pd.Series(ROIfilesList_WE)
    ROIfilesList = pd.Series(ROIfilesList)
    
    #get logics elements to be extracted
    logicToProcess = ROIfilesList_WE.isin(HOGfilesList_WE)
    
    ROIfilesList = ROIfilesList[~logicToProcess]
    #-------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------#
    #if fileHOGpath!='../HOGvectors/':
    #   grp=f.create_group(dir_path[32:])
    #else:
    #    grp=f
    for image in ROIfilesList:
        
        #Extract HOG vectors for image
        I_pathName = os.path.join(dir_path, image)
        
        imgHOGvectors, HOGshape = HOG( cv.imread(I_pathName, cv.IMREAD_GRAYSCALE) ).extractHOG()
        
        #Save imgHOGvectors in fileHOGpath as pd.DataFrame
        csvFileName = os.path.join(fileHOGpath, os.path.splitext(image)[0]+".csv")
        pd.DataFrame(imgHOGvectors).to_csv(csvFileName, index=False, header=False)
        
        
        with h5py.File(os.path.join("..", "..", "variables", "HOG", "HOGallImgs.hdf5"), "a") as f:
            f.create_dataset(image, data=imgHOGvectors)
        
        with h5py.File(os.path.join("..", "..", "variables", "HOG", "HOGshapeAllImgs.hdf5"), "a") as f:
            f.create_dataset(image, data=HOGshape)    
    #-------------------------------------------------------------------------#
 