# Modeling and Simulation of Social Systems Fall 2018 – Research Plan

> * Group Name: Freewalk
> * Group participants names: Bircher Lukas, Martin Christoph, Robin Stähli
> * Project Title: Modelling Human Trail Systems and Implementation in a Real World Problem
> * Programming language: Python

## Introduction

The goal is to show that simulations are able to model the real world to some extent. Therefore a model which can simulate human trail systems was built. The model was tested with basic examples also stated in the paper of Dirk Helbing et al., further expanded to a real world park in Alcala, Spain. 


## The Model

Most of the mathematical model is based on the paper of Dirk Helbing, Joachim Keltsch & Péter Molnàr. It was published in journal Nature in 1997 and is called "Modelling the evolution of human trail systems". There are several variables which can be changed, such as the visibility (which is a value of how far a pedestrian can see the trail), the durability (how fast will the grass regrow or the trail disappear), the amount of pedestrians and the intensity (which is a value of how fast the trail is destroyed by each pedestrian). 
There might be some other aspects we did not capture, such as big groups walking on the field at the same time. This will form wider trails.

## Fundamental Questions

The fundamental question is, whether our model is capable of reflecting trail systems that emerged in the real world. 
(At the end of the project you want to find the answer to these questions)
(Formulate a few, clear questions. Articulate them in sub-questions, from the more general to the more specific. )


## Expected Results

(What are the answers to the above questions that you expect to find before starting your research?)


## References 

(Add the bibliographic references you intend to use)
(Explain possible extension to the above models)
(Code / Projects Reports of the previous year)


## Research Methods

Our model is agent-based. Its goal is to show the interactions between the system and each agent. It is very similar to cellular automata based models, but includes several different agents, in our case pedestrians, which walk on the plain field. 


## Other

We used data found on google earth to display the real world. 

# Reproducibility

(step by step instructions to reproduce your results. *Keep in mind that people reading this should accomplish to reproduce your work within 20 minutes. It needs to be self-contained and easy to use*. e.g. git clone URL_PROY; cd URL_PROY; python3 main.py --light_test (#--light test runs in less than 5minutes with up to date hardware)) 

