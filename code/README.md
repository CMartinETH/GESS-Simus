# Code Folder 

The LIGHT code is used for fast reproducibility with minimal options and minimal functionality.<br>
The LARGE version is able to use the full computing potential (eg. parallelization on the CPU), therefore needs some more toolboxes which need to be downloaded and installed prior to use. <br>
<br>
To use the LIGHT version, the following steps have to be taken:
1. Download the file LIGHT_Triangle_Freewalk.py
2. Make sure you have matplotlib and numpy installed <br>
2.2 If you have installed it already, skip to task 3 <br>
2.1 If you do not have it, you can download and install it by opening a terminal / command line, (activating your environment if you have one) and enter: 
pip install numpy
pip install matplotlib
5. Open your favourite python development environment e.g. PyCharm, Spyder, Jupyter Notebook etc.
6. Open the downloaded file LIGHT_Triangle_Freewalk.py
Important: Do NOT change anything in this file Start the program. It will output every iteration step, up to 500. This might take 1-2 minutes, depending on the CPU of your computer.
When it reaches 500 iterations, it will output a figure (might be in the background). It should show a triangle. This is emerged path of the pedestrians, walking from 3 starting points to a random chosen other end point.



<br>
<br>

To use the LARGE version, the following steps have to be taken:
1. Download the file LARGE_Park_Freewalk.py
2. Move the downloaded files into a folder you want to. Make a folder where you want to save your output. 
Make sure you have the toolboxes matplotlib, numpy, time, timeit, joblib, multiprocessing, and cv2 installed <br>
2.2 If you have installed it already, skip to task 3 <br>
2.1 If you do not have it, you can download and install it by opening a terminal / command line, (activating your environment if you have one) and enter: 
pip install numpy
pip install matplotlib
....
3. Open your favourite python development environment e.g. PyCharm, Spyder, Jupyter Notebook etc.
Open the downloaded file LARGE_Park_Freewalk.py
4. Change the imgpath to the path to the image files you have downloaded. Choose either the original or the green image.
5. Change the newpath to the path of the folder where you want to save your images. 
6. Now you can either change the parameters of the simulation, or start it. It will output the images to the folder you declared. 
7. When it reaches the amount of iterations you chose, it will stop. 
