"""
Created on Tue Jan 21 15:51:40 2020

@author: fernando
"""

import os
import sys
import pandas as pd
import numpy as np
import h5py

currentPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append("{0}/../../PBoW/code".format(currentPath))
from pbow import PBOW

#-----------------------------------------------------------------------------#
#load wordsPerImg.hdf5 and convert to pd.Series
with h5py.File( os.path.join("..", "..", "variables", "PBoW", "imgWords", "wordsPerImg.hdf5"), "r" ) as f:

    wordsPerImglist = list(f.keys())

    pd_wordsPerImg = pd.Series( (np.zeros([len(wordsPerImglist), 300])).tolist(), index=wordsPerImglist )

    for image in wordsPerImglist:
        pd_wordsPerImg[image] = f[image][()]
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Convert the dataset of HOGshapeAllImgs.hdf5 as pd.Series
with h5py.File( os.path.join("..", "..", "variables", "HOG", "HOGshapeAllImgs.hdf5"), "r" ) as f:

    list_ImgsNames = list(f.keys())

    pd_HOGshape = pd.Series( (np.zeros([len(list_ImgsNames), 2])).tolist(), index=list_ImgsNames )

    for image in list_ImgsNames:
        pd_HOGshape[image] = f[image][()]
#-----------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
#Make (if doesn't exist) file PBoWallImgs.hdf5-->all HOG imgs vects
with h5py.File( os.path.join("..", "..", "variables", "PBoW", "PBoWallImgs.hdf5"), "a" ) as f:

    PBoWlist_ImgsNames = list(f.keys())
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Don't consider those imgsWords such that already has been extracted their PBoW

#Convert PBoWlist_ImgsNames and wordsPerImglist in pd.Series
PBoWlist_ImgsNames = pd.Series(PBoWlist_ImgsNames)
wordsPerImglist = pd.Series(wordsPerImglist)

#Extract the logicals elements to be extracted
logicToProcess = wordsPerImglist.isin(PBoWlist_ImgsNames)

wordsPerImglist = wordsPerImglist[~logicToProcess]
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Make and store --> PBoWallImgs.hdf5 (the PBoW for each image)
for image in wordsPerImglist:
    
    hist = ( PBOW(pd_wordsPerImg[image], pd_HOGshape[image]) ).extractPBoW()
    
    #Normalize and store hist in PBoWallImgs.hdf5
    with h5py.File( os.path.join("..", "..", "variables", "PBoW", "PBoWallImgs.hdf5"), "a" ) as f:
        f.create_dataset(image, data=hist)
#-----------------------------------------------------------------------------#
