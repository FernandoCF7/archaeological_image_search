# archaeological_image_search
## **This proyect contais a python software to automatically recover archaeological objects into a image database**
#### Automatic image recovering
#### Archaeological objects recognition
#### Histograms Of Oriented Gradients (HOG)
#### Python
#### HDF5
___
The project image stages are handled by the [OpenCV - Open Computer Vision Library](https://opencv.org/) (with the opencv-contrib-python module), while the data-base image file system is gestioned by the hdf5 (Hierarchical Data Format) approach with the [h5py python module](https://docs.h5py.org/en/stable/). Besides, the project requires other python modules as numpy and pandas, you can check a list of them in the [requirements.txt](/requirements.txt) project file. The image feature extraction is making with the [HOG (Histograms Of Oriented Gradients)](https://www.researchgate.net/publication/281327886_Histograms_of_Oriented_Gradients_for_Human_Detection) algorithm and the indexing step is based on the [PBoW (Pyramid Bag of Words)](https://ieeexplore.ieee.org/document/1238663) method.
___
### Installation and Use
Once you have cloned this repository it's a good practice to make a python enviroment (here called *env*); make it inside the */code* directory
```console
user@foo:~/code$ virtualenv env
```
Activate the enviroment
```console
user@foo:~/code$ source env/bin/activate
```
Install all the python depencendes (modules) with the requirements.txt file
```console
(env)user@foo:~/code$ pip install -r requirements.txt
```
#### The DB image file system
The project includes a */DB* directory, it must store the images to train the system, once you have them (inside the directory) in next stages the system will allow you to create a ROI (Region of Interest) over each image to define the feature extraction area. Note: dosen't mather the file system order inside the DB directory, the program will browse over it; besides, the allowed image format are *.jpg* and *.tif*
#### The ROI stage
To make the ROI (Region of Interest) of the images, run the *code/ROI/code/makeROIthroughDB.py* python file, notice that you can use the *Ipython* interactive console (in the makeROIthroughDB.py path):
```console
(env)user@foo:~/code/ROI/code$ipython
```
Once inside of *Ipython*
```python
In [1]: %run makeROIthroughDB.py
```
This action triggers a interactive window that allows to define the image ROI as a rectangle, see image below
![](/aux_src/ROI_1.png)
![](/aux_src/ROI_2.png)
Once you define the image ROI, the system stores its coordinates and a cropped image with the ROI in the */variables/ROI/coordinates* and */variables/ROI/images* directories, these structure file system replicates the original */DB* structure file system


[//]: # "Contributions"
