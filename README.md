# archaeological_image_search
> ## **This proyect contais a python software to automatically recover archaeological objects into a image database**
> - #### Automatic image recovering
> - #### Archaeological objects recognition
> - #### Histograms Of Oriented Gradients (HOG)
> - #### Python
> - #### HDF5
___
The image project stages are handled by the [OpenCV - Open Computer Vision Library](https://opencv.org/) (with the opencv-contrib-python module). Moreover, the data-base image file system is gestioned by the hdf5 (Hierarchical Data Format) approach with the [h5py python module](https://docs.h5py.org/en/stable/). Besides, the project requires other python modules as numpy and pandas, you can check a list of them in the [requirements.txt](/code/requirements.txt) project file. The image feature extraction is making with the [HOG (Histograms Of Oriented Gradients)](https://www.researchgate.net/publication/281327886_Histograms_of_Oriented_Gradients_for_Human_Detection) algorithm and the indexing step is based on the [PBoW (Pyramid Bag of Words)](https://ieeexplore.ieee.org/document/1238663) method.
___

<video width="630" height="300" src="https://github.com/FernandoCF7/archaeological_image_search/assets/101651797/facbdfee-224d-406b-a36d-deaddc642d1d.mp4"></video>

### Installation and Use

Once you have cloned the repository it's a good practice to make a python enviroment (here called *env*); make it inside the */code* directory
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
#### The database image file system

The project includes a */code/DB* directory, it must store the images to train the system, once you have them (inside the directory) in next stages the system will allow you to create a ROI (Region of Interest) over each image to define the feature extraction area. Note: dosen't mather the file system order inside the DB directory, the program will browse over it; besides, the allowed image format are: *.jpg*, *.jpeg*, *.png*, *.gif*, *.tif*, *.tiff*, *.bmp*, *.webp*, *.pbm*, *.pgm*, *.ppm* and *.exr*

#### Features extraction

The code/system_feature_extraction.py file allows you to run each stage (ROI, HOG and PBOW) to extract the features from each image (at code/DB). Use the *Ipython* interactive console (at the code/ path)
```console
(env)user@foo:~/code/$ipython
```
and run:
```python
In [1]: %run system_feature_extraction.py
```
Note: this process neds the /code/output_src/dictionary/dict_300words.pkl file (stores the image dictionary words of the code/DB images). When you start the project, this file dosen't exist (or if you explicitly deleted it), therefore, the program checks for the file existence and create it if it dosen't exist; but be carfully, once the file exists it will not be remade by this program (code/system_feature_extraction.py), eaven if you update your code/DB image source. Then, to remade the /code/output_src/dictionary/dict_300words.pkl file (the dictionary itself), and gain precision in recovery, you would to run the code/make_or_update_the_dictionary.py program.

#### The ROI stage

The ROI (Region of Interest) of the images is made with the *code/ROI/* module, you can use the *Ipython* (in the code/ROI/makeROIthroughDB.py path) to execute this proces without the code/system_feature_extraction.py interface:
```python
In [1]: %run makeROIthroughDB.py
```
This stage triggers a interactive window that allows to define the ROI image as a rectangle, see image below

![](/aux_src/ROI_1.png)

![](/aux_src/ROI_2.png)

Once you define the ROI image, the system stores its coordinates and a cropped image (the ROI) in the */output_src/ROI/coordinates* and */output_src/ROI/images* directories, these structure file system replicates the original */DB* structure file system

#### HOG extraction

The HOG (Histograms Of Oriented Gradients) feature extraction image is made with the HOG module. The code/HOG/HOG_extraction.py file generates the HOG extraction per image; it will take the ROI images generated in the previous stage. The HOG features are stored using hdf5 methodology at code/output_src/HOG/HOGallImgs.hdf5 and code/output_src/HOG/HOGshapeAllImgs.hdf5

#### Pyramidal Bag of Words (PBoW)

This stage is made with the code/PBoW module. The /code/PBoW/makePBoWperImg.py file takes the default pyramid levels as three (PBOW class /code/PBoW/pbow.py). You can change it at this file (/code/PBoW/makePBoWperImg.py line 64) five in the example below:
```python
hist = ( PBOW(pd_wordsPerImg[image], pd_HOGshape[image], numPyramidLevels=5) ).extractPBoW()
```

#### Dictionary of HOG-words

As said in the 'Features extraction' section, this satage is made when you run the code/system_feature_extraction.py file and the /code/output_src/dictionary/dict_300words.pkl file dosen't exist. If you want to remade the /code/output_src/dictionary/dict_300words.pkl file (the dictionary itself), and gain precision in recovery, you would to run the code/make_or_update_the_dictionary.py program. By dafault, the number of words (clusters) is set to 300, you can change it in the variable n_clusters of MiniBatchKMeans function (/code/make_or_update_dictionary.py) and, in the also change in the /code/PBoW/makePBoWperImg.py and /code/PBoW/pbow.py

#### Recover images

Once these stages have been done, you can recover objects using the code/recover_object.py file. Put the images to recover inside the /code/src_imgs_to_recover directory. Now, the system recover one image at time; just set the image name at the variable image (code/recover_object.py line 26) and run the python file.

[//]: # "Contributions"
