import os
import cv2 as cv
import numpy as np

class BUILT_ROI:
    
    #-------------------------------------------------------------------------#
    def __init__(self, image,dir_path):
        self.image = image
        self.dir_path = dir_path
        self.I_pathName = os.path.join(dir_path,image)
        print(self.I_pathName)
        self.I = cv.imread(self.I_pathName, cv.IMREAD_UNCHANGED)
    #-------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------#
    def makeROI(self):
        
        global drawingRectangle, drawingLine, point1, point2, RectanglePosition
        global askToSave, iterador
        
        #---------------------------------------------------------------------#
        #Set a window image
        cv.namedWindow(self.I_pathName, cv.WINDOW_NORMAL)
        #---------------------------------------------------------------------#
        
        #---------------------------------------------------------------------#
        #bind the callbackMouseEvents and the window image
        cv.setMouseCallback(self.I_pathName, self.callbackMouseEvents)
        #---------------------------------------------------------------------#
        
        #---------------------------------------------------------------------#
        #Define parameters
        drawingRectangle = False
        drawingLine = True
        point1 = ()
        point2 = ()
        RectanglePosition = ()
        #---------------------------------------------------------------------#
        
        #---------------------------------------------------------------------#
        #Display image
        cv.imshow(self.I_pathName, self.I)
        
        iterador = True
        askToSave = False
        
        while iterador:
            
            #-----------------------------------------------------------------#
            #Keyboard events
            key = cv.waitKey(1)
            
            #Quit window ('q')
            if key == ord('q'):
                cv.destroyAllWindows()
                return np.array([]),[]
            
            #reset the selected point1
            if key == 8:#delete key
                drawingRectangle = False
                drawingLine = True
                point1 = ()
                point2 = ()
                RectanglePosition = ()
                cv.imshow(self.I_pathName, self.I)
            #-----------------------------------------------------------------#
            
            #-----------------------------------------------------------------#
            #The ROI was finished-->ask to save or repeat it
            if askToSave:
                
                position1, position2 = self.saveOrReset()
                
                #return the ROI positions [x1,x2,y1,y2] and ROI image
                if len(position1)>0:
                                        
                    x1 = min(position1[0],position2[0])
                    x2 = max(position1[0],position2[0])
                    y1 = min(position1[1],position2[1])
                    y2 = max(position1[1],position2[1])
                                        
                    #Resize image such that diagonal aprox 1000 pixels
                    I_ROI = self.I[y1:y2,x1:x2].copy()
                    
                    diagonal = np.linalg.norm(I_ROI.shape[:2])
                    if diagonal < 800 or diagonal > 1200:
                        scale = 1000/diagonal
                        newSize = (
                            int(I_ROI.shape[:2][1]*scale),
                            int(I_ROI.shape[:2][0]*scale)
                        )
                        I_ROI = cv.resize(I_ROI, newSize)
                    #---------------------------------------------------------#
                    
                    cv.destroyAllWindows()
                    return I_ROI, [x1,x2,y1,y2]
            #-----------------------------------------------------------------#        
    
    #-------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------#
    #Define the Callback events
    def callbackMouseEvents(self, event, x, y, flags, params):
        
        global point1, point2, drawingRectangle, drawingLine, askToSave, RectanglePosition
        
        I_tmp = self.I.copy()
        
        #Draw guide lines at the mouse pointer
        if event == cv.EVENT_MOUSEMOVE and drawingLine == True:
            height, width = self.I.shape[:2]
            cv.line(I_tmp, (x,0), (x,height), (0, 255, 0), 15)
            cv.line(I_tmp, (0,y), (width,y), (0, 255, 0), 15)
            cv.imshow(self.I_pathName, I_tmp)
        
        #Get mouse pointer possition (left mouse button)
        if event == cv.EVENT_LBUTTONDOWN:
            if drawingRectangle is False:
                point1 = (x, y)
                drawingRectangle = True
                drawingLine = False
            else:
                point2 = (x, y)
                drawingRectangle = False
                drawingLine = True
                RectanglePosition = (point1, point2)
                cv.rectangle(I_tmp, point1, point2, (0, 0, 255), 15)
                cv.imshow(self.I_pathName, I_tmp)
                cv.setMouseCallback(self.I_pathName, self.callbackMouseNull)
                askToSave = True
        
        #Draw the rectangle
        elif event == cv.EVENT_MOUSEMOVE and drawingRectangle == True:
            point2 = (x,y)
            cv.rectangle(I_tmp, point1, point2, (0, 255, 0), 15)
            cv.imshow(self.I_pathName, I_tmp)
    #-------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------#
    #Dumb function to hold on the selected rectangle
    def callbackMouseNull(self, event, x, y, flags, params):
        pass
    #-------------------------------------------------------------------------#
            
    #-----------------------------------------------------------------------------#
    #Function to reset the callbackMouseEvents functions    
    def saveOrReset(self):
        global point1, point2, RectanglePosition, iterador, askToSave
        
        print('accept? Yes=Into; No=Supr')
    
        while True:
            
            key = cv.waitKey()# & 0b11111111 
            
            if key == 13:#Save-->Intro
                iterador = False
                break
            
            elif key == 255:#Reject-->Supr
                point1 = ()
                point2 = ()
                RectanglePosition = ()
                askToSave = False
                cv.imshow(self.I_pathName, self.I)
                cv.setMouseCallback(self.I_pathName, self.callbackMouseEvents)
                break
        
        return point1, point2
    #-----------------------------------------------------------------------------#        
