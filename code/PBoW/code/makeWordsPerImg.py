"""
Created on Mon Jan 20 21:21:38 2020

@author: fernando
"""

#-----------------------------------------------------------------------------#
import os
import pandas as pd
import h5py
import pickle
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#load the dictionary
kmeans = pickle.load( open(os.path.join("..", "..", "variables", "dictionary", "dict_300words.pkl"), "rb") )
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Load the HOG vectors imgs names
with h5py.File( os.path.join("..", "..", "variables", "HOG", "HOGallImgs.hdf5"), "r" ) as f:
    HOGlist_ImgsNames = list(f.keys())
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Read or make, if doesn't exist, the wordsPerImg.plk file
with h5py.File( os.path.join("..", "..", "variables", "PBoW", "imgWords", "wordsPerImg.hdf5"), "a" ) as f:
    wordsPerImg_List = list(f.keys())
#-----------------------------------------------------------------------------#
    
#-----------------------------------------------------------------------------#
#Don't consider those HOG imgs vectors that already has been extracted their words 

#Convert wordsPerImg_List and HOGlist_ImgsNames in pd.Series
wordsPerImg_List = pd.Series(wordsPerImg_List)
HOGlist_ImgsNames = pd.Series(HOGlist_ImgsNames)

#Extract the logicals elements to be extracted
logicToProcess = HOGlist_ImgsNames.isin(wordsPerImg_List)

HOGlist_ImgsNames = HOGlist_ImgsNames[~logicToProcess]
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
with h5py.File( os.path.join("..", "..", "variables", "HOG", "HOGallImgs.hdf5"), "a" ) as f:
    
    with h5py.File( os.path.join("..", "..", "variables", "PBoW", "imgWords", "wordsPerImg.hdf5"), "a" ) as g:
        
        for image in HOGlist_ImgsNames:
            print(image)
            g.create_dataset( image, data=kmeans.predict(f[image][()]) )        
#-----------------------------------------------------------------------------#
