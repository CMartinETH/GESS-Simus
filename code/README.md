# Code Folder 

The LIGHT code is used for fast reproducibility with minimal options and minimal functionality. There is a step by step guide in the overall README file. <br>
The LARGE version is able to use the full computing potential (eg. parallelization on the CPU), therefore needs some more toolboxes which need to be downloaded and installed prior to use. <br>
To use the LARGE version, the following steps have to be taken:
1. Download the file LIGHT_Triangle_Freewalk.py
Make sure you have matplotlib and numpy installed 
2.2 If you have installed it already, skip to task 3
2.1 If you do not have it, you can download and install it by opening a terminal / command line, (activating your environment if you have one) and enter: 
pip install numpy
pip install matplotlib
Open your favourite python development environment e.g. PyCharm, Spyder, Jupyter Notebook etc.
Open the downloaded file LIGHT_Triangle_Freewalk.py
Important: Do NOT change anything in this file Start the program. It will output every iteration step, up to 500. This might take 1-2 minutes, depending on the CPU of your computer.
When it reaches 500 iterations, it will output a figure (might be in the background). It should show a triangle. This is emerged path of the pedestrians, walking from 3 starting points to a random chosen other end point.
