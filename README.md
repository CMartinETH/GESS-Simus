# Modeling and Simulation of Social Systems Fall 2018 – Research Plan

> * Group Name: Freewalk
> * Group participants names: Bircher Lukas, Martin Christoph, Robin Stähli
> * Project Title: Modelling Human Trail Systems and Implementation in a Real World Problem
> * Programming language: Python

## Introduction

The goal is to show that simulations are able to model the real world to some extent. Therefore a model which can simulate human trail systems was built. The model was tested with basic examples also stated in the paper of Dirk Helbing et al., further expanded to a real world park in Alcala, Spain. 

## Reproducibility

1.    Download the file LIGHT_Triangle_Freewalk.py
2.    Make sure you have matplotlib and numpy installed <br>
  2.2 If you have installed it already, skip to task 3<br>
  2.1   If you do not have it, you can download and install it by opening a terminal / command line, (activating your 
        environment if you have one) and enter:     <br>
        pip install numpy<br>
        pip install matplotlib
3.    Open your favourite python development environment e.g. PyCharm, Spyder, Jupyter Notebook etc. 
4.    Open the downloaded file LIGHT_Triangle_Freewalk.py  
      Important: Do NOT change anything in this file
      Start the program. It will output every iteration step, up to 500. This might take 1-2 minutes, depending on the CPU of 
      your computer.
5.    When it reaches 500 iterations, it will output a figure (might be in the background). It should show a triangle. This is
      emerged path of the pedestrians, walking from 3 starting points to a random chosen other end point. 

## The Model

Most of the mathematical model is based on the paper of Dirk Helbing, Joachim Keltsch & Péter Molnàr. It was published in journal Nature in 1997 and is called "Modelling the evolution of human trail systems". There are several variables which can be changed, such as the visibility (which is a value of how far a pedestrian can see the trail), the durability (how fast will the grass regrow or the trail disappear), the amount of pedestrians and the intensity (which is a value of how fast the trail is destroyed by each pedestrian). <br>
There might be some other aspects we did not capture, such as big groups walking on the field at the same time. This will form wider trails.

## Fundamental Questions

The fundamental question is, whether our model is capable of reflecting trail systems that emerged in the real world. Before it is tested on a real problem, it should be evaluated on a test case, similar to the one Dirk Helbing et al. used in their paper. So this question should answer the overall capability of the program. <br>
For further reproduction of the real world case, one certain park was chosen.<br>
The last question is, what effect does the visibility have on the outcome of the simulation. 

## Results

The code definitely works and delivers similar results to the paper of Dirk Helbing et al., therefore the further tests on the real world case were done.<br>
The real world problem shows that the model is accurate, but depends strongly on the boundary conditions. <br>
These tests also show the effect of the visibility on the outcome. It has the largest effect on the system. The type of emerging way system depends upon the chosen visibility (sigma). 


## References 


Dirk Helbing, Joachim Keltsch & Péter Molnàr. <br> 
Modelling the evolution of human trail systems. <br>
Macmillan Publishers Ltd, Nature, 1997.


## Research Methods

Our model is agent-based. Its goal is to show the interactions between the system and each agent. It is very similar to cellular automata based models, but includes several different agents, in our case pedestrians, which walk on the plain field. 


## Other

We used data found on google earth to display the real world. 



