"""
run this file to add at the proceess the new images added to the /code/DB
Created on Fri Jan 24 20:10:31 2020

@author: fernando
"""
#-----------------------------------------------------------------------------#
import os

#-----------------------------------------------------------------------------#
#make ROI
exec(open(os.path.join("ROI", "makeROIthroughDB.py")).read())
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Make and append the HOG vectors
exec(open(os.path.join("HOG", "HOG_extraction.py")).read())
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Make the dictionary if it does not exist
if not os.path.exists(os.path.join("output_src", "dictionary", "dict_300words.pkl")):
    exec(open(os.path.join("make_or_update_the_dictionary.py")).read())
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Make and append word per image
exec(open(os.path.join("PBoW", "makeWordsPerImg.py")).read())
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#Make and append Make word per image
exec(open(os.path.join("PBoW", "makePBoWperImg.py")).read())
#-----------------------------------------------------------------------------#