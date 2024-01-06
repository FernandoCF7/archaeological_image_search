"""
Created on Wed Jan 22 19:42:00 2020

@author: fernando
"""
#-----------------------------------------------------------------------------#
import os
import sys
import cv2 as cv
import h5py
import pickle
import pandas as pd
import numpy as np

sys.path.append("./ROI")
sys.path.append("./HOG")
sys.path.append("./PBoW")
from built_roi import BUILT_ROI
from hog import HOG
from pbow import PBOW
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
#Image to recover IMG_20200125_125102306.jpg
image = "IMG_20190711_113515544.jpg"

#image path
pathImage = os.path.join("./src_imgs_to_recover")
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#built ROI image
I_ROI, ROIcoordinates = BUILT_ROI(image, pathImage).makeROI()

#Convert I_ROI BGR2GRAY
if len(I_ROI.shape) == 3:
    I_ROI = cv.cvtColor(I_ROI, cv.COLOR_BGR2GRAY)
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Extract HOG vectors
if I_ROI.size != 0:
    imgHOGvectors, HOGshape = HOG(I_ROI).extractHOG()
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Extract image words

#load the dictionary
kmeans = pickle.load( open(os.path.join("output_src", "dictionary", "dict_300words.pkl"), "rb") )

pd_wordsPerImg = pd.Series( [kmeans.predict(imgHOGvectors)], index=[image] )
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Extract PBoW image
hist = (PBOW(pd_wordsPerImg[image], HOGshape)).extractPBoW()
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
#Extract the k-BBF (Best Bin First) algorithm

#Load the stored PBoWallImgs.hdf5 and convert to np
with h5py.File( os.path.join("output_src", "PBoW", "PBoWallImgs.hdf5"), "r" ) as f:

    list_ImgsNames=list(f.keys())
    np_PBoWallImgs = np.empty((len(list_ImgsNames), 4200))

    count=0
    for image in list_ImgsNames:
        np_PBoWallImgs[count] = f[image][()]
        count+=1

#Extract distances
distance = np.linalg.norm( np_PBoWallImgs-hist, axis=1 )

#Sorted list
list_ImgsNames = np.array(list_ImgsNames)
sortedList = list_ImgsNames[np.argsort(distance)]

#Display the first near neibghour
path_firstImg = os.path.join( "DB","{0}".format(sortedList[0]) )
firstImg = cv.imread(path_firstImg, cv.IMREAD_UNCHANGED)
cv.namedWindow("recovered image", cv.WINDOW_NORMAL)
cv.imshow("recovered image", firstImg)
cv.waitKey(0)
cv.destroyAllWindows()
