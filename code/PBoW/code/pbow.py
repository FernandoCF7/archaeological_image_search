"""
Created on Thu Jan 23 16:07:09 2020

@author: fernando
"""
import numpy as np

class PBOW:

    def __init__(self, words, HOGsahape, numPyramidLevels=3, numWordsInDic=300):
        self.words = words
        self.HOGsahape = HOGsahape
        self.numPyramidLevels = numPyramidLevels
        self.numWordsInDic = numWordsInDic
        
    
    def extractPBoW(self):
        
        wordsInDic = np.empty( (self.numWordsInDic, 1, 1) )
        wordsInDic[:, -1, -1] = np.arange(0, self.numWordsInDic)
        
        #Reshape words as pd_HOGshape[image] values
        words = self.words.reshape(self.HOGsahape)
        
        #Predefine np array to store the PBoW
        hist = ( np.empty((1, 0)) ).astype(int)
        
        #Make the BoW through each pyramid level
        for L in range(self.numPyramidLevels):#L (level) --> [0, 1, 2, ..., numPyramidLevels-1]
            
            #Split the matrix words as the blocks generated by the pyramid
            wordsSegmentedByColumn = np.array_split(words, L+1, axis=1)
            
            #Store the words from each block in a row of pd.DataFrame
            M, N = self.HOGsahape[:]
            numWordsPerBlock = int( np.ceil(M/(L+1))*np.ceil(N/(L+1)) )
            
            imgWordsPerBlock = np.full( [(L+1)**2, numWordsPerBlock], np.nan )

            counter = 0
            for wordsColumn in wordsSegmentedByColumn:
                
                wordsColumnRows = np.asarray( np.array_split(wordsColumn, L+1, axis=0) )
                
                for wordsPerBlock in wordsColumnRows:
                    wordsPerBlock = wordsPerBlock.reshape(1, -1)
                    
                    imgWordsPerBlock[counter, 0:wordsPerBlock.size] = wordsPerBlock

                    counter += 1
                    
            #Make the BoW taking into account imgWordsPerBlock matrix
            hist_piramidLevel = (imgWordsPerBlock==wordsInDic).sum(axis=2)
            hist = np.hstack( (hist, hist_piramidLevel.swapaxes(1, 0).reshape(1, -1)) )
            
        #Normalize and return hist
        return hist/np.linalg.norm(hist)
            
            
            
            
            
            
            
            