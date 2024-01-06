"""
Created on Mon Jan 20 12:50:32 2020

@author: fernando
"""

#-----------------------------------------------------------------------------#
import os
import h5py
from sklearn.cluster import MiniBatchKMeans
import pickle
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Make the dictionary
with h5py.File(os.path.join("output_src", "HOG", "HOGallImgs.hdf5"), "r") as f:
    list_ImgsNames = list(f.keys())
    
    kmeans = MiniBatchKMeans(
        n_clusters=300,
        init='k-means++',
        random_state=0,
        compute_labels=False
    ).fit( f[list_ImgsNames[0]][()] )
    
    for image in list_ImgsNames[1:]:
        kmeans.partial_fit( f[image][()] )
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Store the dictionary
pickle.dump(
    kmeans,
    open(os.path.join("output_src", "dictionary", "dict_300words.pkl"), "wb")
)
#-----------------------------------------------------------------------------#
