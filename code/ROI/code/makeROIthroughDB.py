import os
import sys
import cv2 as cv
import pandas as pd

#Add to sys.path the path to ROI/code
currentPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append("{0}/../../ROI/code".format(currentPath))

from built_roi import BUILT_ROI

#-----------------------------------------------------------------------------#
#browse into image directory
for dir_path, dir_names, image_names in os.walk(os.path.join("..", "..", "DB")):
    
    #-------------------------------------------------------------------------#
    #Create the csv file (if no exist) to store the ROIcoordinates
    
    #Set filename as current dir_path
    fileName = dir_path[9:].replace(os.path.sep,"_")
    filePath = os.path.join("..", "..", "variables", "ROI", "coordinates", "{0}ROIcoordinates.csv".format(fileName))
    
    if os.path.isfile(filePath) == False:
        with open( filePath, "w" ) as f:
            #Set headers
            f.write("imageName,x1,y1,x2,y2\n")        
    #-------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------#
    #Create the directory (if no exist) to store the ROI images
    ROIdirectoryPath = os.path.join("..", "..", "variables", "ROI", "images", "{0}".format(dir_path[9:]))
    
    #Ask if directory exist
    if os.path.isdir(ROIdirectoryPath) == False:
        os.mkdir(ROIdirectoryPath)
    #-------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------#
    #ignore those images that their ROI has been extracted
    #To CSV file
    if os.path.isfile(filePath):
        pd_csvFile = (pd.read_csv(filePath, usecols=["imageName"]))
        image_names_inDB = pd.Series(image_names)
        logicExistImgs_CSV = image_names_inDB.isin(pd_csvFile['imageName'])
    
    #To ROIdirectoryPath
    if os.path.isdir(ROIdirectoryPath):
        image_namesInROIdirectoryPath = next(os.walk(ROIdirectoryPath))[2]
        image_names_inDB = pd.Series(image_names)
        logicExistImgs_ROI = image_names_inDB.isin(image_namesInROIdirectoryPath)
    
    #Update image_names
    if os.path.isfile(filePath) | os.path.isdir(ROIdirectoryPath):
        image_names = image_names_inDB[~logicExistImgs_CSV | ~logicExistImgs_ROI].tolist()
        image_namesToRemplaceInCSVfile = image_names_inDB[logicExistImgs_CSV & ~logicExistImgs_ROI].tolist()
    #-------------------------------------------------------------------------#
    
    #-------------------------------------------------------------------------#
    #Make ROI for each element in image_names
    csvUpdateRegister = []
    for image in image_names:
        
        I_ROI, ROIcoordinates = BUILT_ROI(image, dir_path).makeROI()
        
        #Save I_ROI and ROIcoordinates
        if I_ROI.size != 0:
            
            #save RectanglePosition in the .csv file
            if image in image_namesToRemplaceInCSVfile:#Remplace
                
                #Open filePath with pd.read_csv
                pd_csvFile = (pd.read_csv(filePath))
                
                #find image in pd_csvFile
                pd_csvFile.at[pd_csvFile["imageName"] == image,1:5] = ROIcoordinates
                pd_csvFile.to_csv(filePath, index=False)
                
            else:#insert
                x1,x2 = ROIcoordinates[0], ROIcoordinates[1]
                y1,y2 = ROIcoordinates[2], ROIcoordinates[3]
                csvUpdateRegister.append("{0},{1},{2},{3},{4}\n".format(image,x1,y1,x2,y2))
            
            #Save the ROI image into directoryPath directory
            cv.imwrite(os.path.join(ROIdirectoryPath, image), I_ROI)
            #---------------------------------------------------------#
     
    #drop off the csvUpdateRegister content into filePath
    with open(filePath, "a") as f:
        f.writelines(csvUpdateRegister)
    #-------------------------------------------------------------------------#

else:
    print("Finish, no more images to process")