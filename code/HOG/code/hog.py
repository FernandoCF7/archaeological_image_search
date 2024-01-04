"""
Created on Fri Jan 17 19:09:32 2020

@author: fernando
"""

#-----------------------------------------------------------------------------#
import cv2 as cv
import numpy as np
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
class HOG:
    
    sizeCell = 8# --> 8X8 pixels
    sizeBlock = 2# --> 2X2 blocks
    histBins = np.arange(0, 180, 20)#[0,20,40,...,160]
    
    def __init__(self, I):
        self.I = I
        
        #Cut I, such that its height and width will bee multipler of 8
        self.I_height, self.I_width = self.I.shape[:2]

        if self.I_height%8 != 0:
            self.I = np.delete(self.I, np.s_[-(self.I_height%8):], 0)            
            self.I_height = self.I.shape[0]
        if self.I_width%8 != 0:
            self.I = np.delete(self.I, np.s_[-(self.I_width%8):], 1)
            self.I_width = self.I.shape[1]
    
    def extractHOG(self):
        
        #---------------------------------------------------------------------#
        #Gradient
        grad_x = cv.Sobel(self.I, cv.CV_32F, 1,0, ksize=1)
        grad_y = cv.Sobel(self.I, cv.CV_32F, 0,1, ksize=1)
        
        #Gradient magnitude and direction (in degrees)
        mag, angle = cv.cartToPolar(grad_x, grad_y, angleInDegrees=True)

        #Set angle as [0,180]
        angle[angle>180] = 360-angle[angle>180]
        
        angleIn20 = angle/20
        HOGcells_x = int(self.I_width/8)
        HOGcells_y = int(self.I_height/8)
        #---------------------------------------------------------------------#
        
        #---------------------------------------------------------------------#
        #his--> histogram per image 8X8 cell
        
        #Reshape as NumCellsX64; tracking: 1rst-->height and 2nd-->width
        angleIn20 = np.split(angleIn20, self.I_width/8, axis=1)
        angleIn20 = np.asarray(angleIn20)
        angleIn20 = angleIn20.reshape(int((self.I_width/8)*(self.I_height/8)), 64)
        
        mag = np.split(mag, self.I_width/8, axis=1)
        mag = np.asarray(mag)
        mag = mag.reshape(int((self.I_width/8)*(self.I_height/8)), 64)
        
        floor_angle = np.floor(angleIn20)
        percentToCeil = angleIn20-floor_angle
        percentToFloor = 1-percentToCeil
        
        magToFloor = np.floor(percentToFloor*mag)
        magToCeil = np.floor(percentToCeil*mag)
        
        ceil_angle = floor_angle+1
        floor_angle[floor_angle==9] = 0
        ceil_angle[ceil_angle==9] = 0
        ceil_angle[ceil_angle==10] = 1
        
        #lTC-->logicToComput
        #       allows to compute just cells that have almost one element (efficency)
        lTC = magToFloor.any(axis=1) | magToCeil.any(axis=1)
        
        his = np.zeros([floor_angle.shape[0], 9])
        for c1 in np.arange(0,9):
            his[lTC,c1] = ((floor_angle[lTC,:]==c1)*magToFloor[lTC,:]).sum(axis=1) + ((ceil_angle[lTC,:]==c1)*magToCeil[lTC,:]).sum(axis=1)
        #---------------------------------------------------------------------#
        
        #---------------------------------------------------------------------#
        #Make the block cells-->histogram 36 bin
        
        #(x, y) coordinates from cells
        xCell = np.arange(0, HOGcells_x-1).astype(int)
        yCell = np.arange(0, HOGcells_y-1).astype(int)
        
        #meshgrid xCell, yCell
        xCell, yCell = np.meshgrid(xCell,yCell)
        xCell = xCell.swapaxes(0,1).reshape(int((HOGcells_x-1)*(HOGcells_y-1)))
        yCell = yCell.swapaxes(0,1).reshape(int((HOGcells_x-1)*(HOGcells_y-1)))
        
        #[xCell,yCell] sub2indice-->ravel_multi_index
        upLeft = np.ravel_multi_index( np.array([xCell,yCell]), (HOGcells_x, HOGcells_y) )
        downLeft = np.ravel_multi_index( np.array([xCell,yCell+1]), (HOGcells_x, HOGcells_y) )
        upRight = np.ravel_multi_index( np.array([xCell+1,yCell]), (HOGcells_x, HOGcells_y) )
        downRight = np.ravel_multi_index( np.array([xCell+1,yCell+1]), (HOGcells_x, HOGcells_y) )
        
        #Make the HOG matrix, each row represents one block
        img_HOG = np.concatenate( (his[upLeft], his[downLeft], his[upRight], his[downRight]), axis=1 )
        
        #Normalize img_HOG (normaliza each row)
        LTC = img_HOG.any(axis=1)
        norms = np.linalg.norm(img_HOG[LTC,:],axis=1)
        img_HOG[LTC,:] = (img_HOG[LTC,:].swapaxes(0,1)/norms).swapaxes(0,1)
        #---------------------------------------------------------------------#
        
        return img_HOG, np.array([HOGcells_y-1, HOGcells_x-1])
        
        
        
        
        
        
        