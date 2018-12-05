import numpy as np
import matplotlib.pyplot as plt
import random
import os
import matplotlib
from os import path
import time
from joblib import Parallel, delayed
import multiprocessing
import cv2
import timeit

run_time = time.strftime("%Y%m%d_%H%M") ## Time of Run of the programm, will be used for the name of the folder


##############################################################################
## To do first!
## 1.Write correct path 'imgpath' for load file of park and save data 'newpath' 
## 2.Choose your parameter in the sequence of parameter
## 3.If you want simulate other parks than Alcala change respwan points (p0) in function respwan(pedestrians)
##############################################################################


##############################################################################
## Path to load and save file
## Write correct path 'imgpath' for load file of park and save data 'newpath' 
## Example:

## Example for mac 
imgpath = '/Users/username/folder/Alcala_green.png' ## loads file from park you want to evaluate
newpath = r'/Users/username/folder/images/{}'.format(run_time) ## saves all generated data in this folder

## For Windows

#imgpath = "C:\\Users\\Lukas\\Documents\\1_Schule\\Modelling_and_Simulating_Social_Systems\\Alcala_130xpx_137yps.png"## loads file from park you want to evaluate
#newpath = "C:\\Users\\Lukas\\Documents\\1_Schule\\Modelling_and_Simulating_Social_Systems\\Test_Save_Plot\{}".format(run_time) ## saves all generated data in this folder

############################################################################## 


##############################################################################
## Parameters for run
## Choose your parameter in the sequence of parameter
iterations = 800  # amount of cycles
Intensity = 0.35  # Destruction of Trail (I)
Durability = 2000  # Growth rate / regeneration (T) The higher, the slower the grass grows
sigma = 12  # Visibility
v0 = 1  # Velocity of pedestrian 
ped_num = 10  # Number of Pedestrians 

##############################################################################


##############################################################################
## observe dimensions of park you want to evaluate and prepars pic for model
img = cv2.imread(imgpath,0) # read in file of park to matrix (grayscale)
Parkshape = img.shape #size of image
print("Pixel size of the park: ",Parkshape) 
img = img/255 # color of pixel (RGB) to value between 0 to 1
invmat = np.ones([Parkshape[0],Parkshape[1]]) # Matrix with ones in size of immge
ParkMat = invmat-img # Invertion of image of park 
Pedestrianrecord = np.zeros([Parkshape[0],Parkshape[1]]) # generats map were pedestrian have walked during the hole run

##############################################################################


##############################################################################
##initialization of data for main
pedestrians = np.ones((ped_num, 4))  # Array where the start/actual-x postition, start/actual-y postition, destination-x und destination-y position of pedestrian are saved
field = Parkshape  # field area
G_0 = ParkMat  # ground structure
G_akt = ParkMat  # actual ground structure
G_max = np.asarray(np.ones((field[0], field[1]), dtype=float))  # max of ground structure
## intialization of data for multithreding process
num_cores = multiprocessing.cpu_count() # read in number of your cpu cores
print("Number of your cpu cores: ",num_cores)
##############################################################################


##############################################################################
## generates new folder to save data 
if not os.path.exists(newpath):
    os.makedirs(newpath)
##############################################################################


##############################################################################
## generates a log file and write in all characteristics of the run    
kappa = (Intensity * Durability) / sigma
Lambda = (v0 * Durability) / sigma

file = os.path.join(newpath, "Run_Characteristic.txt")
file1 = open(file, "w")
file1.write("Date and Time: {0}\n".format(run_time))
file1.write("Intensity: {0}\n".format(Intensity))
file1.write("Durability: {0}\n".format(Durability))
file1.write("Sigma: {0}\n".format(sigma))
file1.write("V0: {0}\n".format(v0))
file1.write("Kappa: {0}\n".format(kappa))
file1.write("Lambda: {0}\n".format(Lambda))
file1.write("Field Size: {0}\n".format(field))
file1.write("Number of Pedestrians: {0}\n".format(ped_num))
file1.write("Iterations: {0}\n".format(iterations))
file1.close()
##############################################################################


##############################################################################
## Function calculates equation of environmental changes and calculation of new ground structure
##
## Inputs: Intensitiy; Durability; G_0 (Ground structure); G_akt (actual field structure), G_max (max of ground structure); pedestrians
## Outputs: G_akt (actual field structure)
def dG(intens, durab, g0, g_ak, g_m, ped):
    d_g = np.asarray(np.zeros((field[0], field[1]), dtype=float)) # Array to save changes of ground structure
    d_g1 = 1 / durab * np.asarray(g0 - g_ak) # Calculates regeneration of ground structure
    g_ak = g_ak + d_g1 # Update actual ground structure
    i = 0
    while i < (ped.shape[0]): # for all pedestirans
        x = int(round(ped[i, 0]))
        y = int(round(ped[i, 1]))
        d_g[x, y] = intens * (1 - (g_ak[x, y] / g_m[x, y])) # Calculates distruction of pedestrians
        i = i + 1
        g_ak[x, y] = d_g[x, y] + g_ak[x, y]# Update of actual ground structure
    return g_ak
##############################################################################
    


##############################################################################
## Sub-Function calculates trail potential
##
## Inputs: x and y position to calculate trail potential; Sigma (Visibility); G_akt (actual field structure), 
## Outputs: vtr (trail potential)
def d_r(x, y, G_ak, sig):
    vtr = 0
    for i in range(0, field[0]):
        for k in range(0, field[1]):
            dist = np.sqrt((i - x) ** 2 + (k - y) ** 2) # distance calculation for trail potential
            vtr = vtr + np.exp(-dist / sig) * G_ak[i, k] # trail potential calculation
    vtr = vtr/(field[0]*field[1])    #scaling to field size
    return vtr
##############################################################################
    

##############################################################################
## Sub-Function calculates derivation of trail potential in vertical direction
##
## Inputs: i (number of pedestrian to calculate derivation); pedestrian ; Sigma (Visibility); G_akt (actual field structure) 
## Outputs: derivation of vtr (trail potential) in vertical direction
def vec_parallel_vt1(i, ped, G_ak, sig):
    x = int(round(ped[i, 0]))
    y = int(round(ped[i, 1]))
    Vtr1 = d_r(x + 1, y, G_ak, sig)
    Vtr3 = d_r(x - 1, y, G_ak, sig)
    dVtr1 = (Vtr1 - Vtr3) / 2
    return dVtr1
##############################################################################
    

##############################################################################
## Sub-Function calculates derivation of trail potential in horizontal direction
##
## Inputs: i (number of pedestrian to calculate derivation); pedestrian ; Sigma (Visibility); G_akt (actual field structure) 
## Outputs: derivation of vtr (trail potential) in horziontal direction
def vec_parallel_vt2(i, ped, G_ak, sig):
    x = int(round(ped[i, 0]))
    y = int(round(ped[i, 1]))
    Vtr2 = d_r(x, y + 1, G_ak, sig)
    Vtr4 = d_r(x, y - 1, G_ak, sig)
    dVtr2 = (Vtr2 - Vtr4) / 2
    return dVtr2
##############################################################################
    

##############################################################################
## Sub-Function calculates vertical part of vector to destination of pedestrian
##
## Inputs: i (number of pedestrian to calculate destination vector); pedestrian
## Outputs: d_dest1(vertical part of vector to destination of pedestrian)
def vec_parallel_d1(i, ped):
    d_dest1 = ped[i, 2] - ped[i, 0]
    return d_dest1
##############################################################################
    

##############################################################################
## Sub-Function calculates horizontal part of vector to destination of pedestrian
##
## Inputs: i (number of pedestrian to calculate destination vector); pedestrian
## Outputs: d_dest2 (horizontal part of vector to destination of pedestrian)
def vec_parallel_d2(i, ped):
    d_dest2 = ped[i, 3] - ped[i, 1]
    return d_dest2
##############################################################################
    

##############################################################################
## Function is used to parallelize the calculation of the pedestrian direction and calls with multicore operataion the Sub-Functions
##
## Inputs:  pedestrian ; Sigma (Visibility); G_akt (actual field structure) 
## Outputs: Columne of all calculated vectors
def vec(ped, G_ak, sig):
    results1 = Parallel(n_jobs=num_cores)(delayed(vec_parallel_vt1)(i, ped, G_ak, sig) for i in range(0, ped.shape[0]))
    results2 = Parallel(n_jobs=num_cores)(delayed(vec_parallel_vt2)(i, ped, G_ak, sig) for i in range(0, ped.shape[0]))
    results3 = Parallel(n_jobs=num_cores)(delayed(vec_parallel_d1)(i, ped) for i in range(0, ped.shape[0]))
    results4 = Parallel(n_jobs=num_cores)(delayed(vec_parallel_d2)(i, ped) for i in range(0, ped.shape[0]))
    d_Vtr = np.column_stack((results1, results2)) #Stacks vector of trail potentials
    d_dest = np.column_stack((results3, results4)) #Stacks vector of destination
    return {"d_dest": d_dest, "d_Vtr": d_Vtr} #Columne of all calculated vectors
##############################################################################
    

##############################################################################
## Function calculates the effective vector of the pedestrian displacement
##
## Inputs:  pedestrian ; Sigma (Visibility); G_akt (actual field structure); v0 (pedestrian velocity) 
## Outputs: epdest (all pedestrians displacement vectors)
def d_pos(ped, G_ak, sig, v0):
    epdest = np.zeros((ped.shape[0], 2), dtype=float)
    result= vec(ped, G_ak, sig)
    d_dest = result["d_dest"]
    dVtr = result["d_Vtr"]
    for i in range(0, ped.shape[0]):
        length_dest = np.sqrt((d_dest[i, 0]) ** 2 + (d_dest[i, 1]) ** 2) #length destination vector
        length_pot = np.sqrt((dVtr[i, 0]) ** 2 + (dVtr[i, 1]) ** 2) #length trail potential vector
        if length_dest == 0:
            d_dest[i, :] = d_dest[i,:]
        else:
            d_dest[i, :] = d_dest[i, :] / length_dest #standardization of destination vector if >0
        dVtr[i, :] = dVtr[i, :] / length_pot #standardization of trail potential vector

        d_dest = d_dest * 1.5 # prioritization of destination vector to ensure that pedestrian reaches destination
        lengthl = np.sqrt((d_dest[i, 0] + dVtr[i, 0]) ** 2 + (d_dest[i, 1] + dVtr[i, 1]) ** 2) #length of combined vector (destination + potential vector)
        epdest[i, 0] = (d_dest[i, 0] + dVtr[i, 0]) / (lengthl) * v0 # pedestrian vertical displacement vector
        epdest[i, 1] = (d_dest[i, 1] + dVtr[i, 1]) / (lengthl) * v0 # pedestrian horizontal displacement vector
    return epdest
##############################################################################
    

##############################################################################
## Function for respawning of the pedestrians when they reach their destination 
## Attention respwan point are spezific for park
## Inputs:  pedestrian
## Outputs: pedestrian (updated pedestrian array)
def respawn(ped):
    for i in range(0, ped.shape[0]):
        p_0 = [[3, 3], [6, 3], 
               [Parkshape[0] - 3, 22], [Parkshape[0] - 3, 25],
               [Parkshape[0] - 3, Parkshape[1] / 3 * 2 - 12], [Parkshape[0] - 3, Parkshape[1] / 3 * 2 - 15],
               [Parkshape[0] - 3, Parkshape[1] / 3 * 2 - 18], [Parkshape[0] - 3, Parkshape[1] / 3 * 2 - 21],
               [Parkshape[0] - 3, Parkshape[1] / 3 * 2 - 12], [Parkshape[0] - 3, Parkshape[1] / 3 * 2 - 15],
               [Parkshape[0] - 3, Parkshape[1] / 3 * 2 - 18], [Parkshape[0] - 3, Parkshape[1] / 3 * 2 - 21],
               [Parkshape[0] - 3, Parkshape[1] - 13], [Parkshape[0] - 3, Parkshape[1] - 16],
               [3, Parkshape[1] - 3], [3, Parkshape[1] - 6], [3, Parkshape[1] - 9], [3, Parkshape[1] - 12],
               [3, Parkshape[1] - 3], [3, Parkshape[1] - 6], [3, Parkshape[1] - 9], [3, Parkshape[1] - 12],
               [3, Parkshape[1] / 5 * 2], [3, Parkshape[1] / 5 * 2 + 3]]                                        #respwan points specifig for park alcala

        if (abs(round(ped[i, 0]) - round(ped[i, 2]))) < 1.5 and abs(round(ped[i, 1]) - round(ped[i, 3])) < 1.5: #when pedestrian reach destination

            ped[i, 0], ped[i, 1] = random.choice(p_0) #random choice of location in p0 for start position
            ped[i, 2], ped[i, 3] = random.choice(p_0) #random choice of location in p0 for destination position
            while ((ped[i, 0] == ped[i, 2]) and (ped[i, 1] == ped[i, 3])): # prohibits that destination is equal to start
                ped[i, 2], ped[i, 3] = random.choice(p_0)
    return ped
##############################################################################
    

##############################################################################
##############################################################################
## main from which all the functions are called
pic_number = 1 # image number
start = timeit.timeit() # start counter
for j in range(0, iterations):
    respawn(pedestrians) # respawn pedestrians that reched the destination
    start = time.perf_counter()
    G_akt = dG(Intensity, Durability, G_0, G_akt, G_max, pedestrians) # update the field matrix
    d_v = d_pos(pedestrians, G_akt, sigma, v0) # calculate walking direction of all pedestrians
    for i in range(0, pedestrians.shape[0]): # update the prositions of the pedestrians
        pedestrians[i, 0] = pedestrians[i, 0] + d_v[i, 0]
        pedestrians[i, 1] = pedestrians[i, 1] + d_v[i, 1]
        if j == (iterations-1):   
            pedestrians[i, 0], pedestrians[i, 1] = [2,2]
        Pedestrianrecord[int(pedestrians[i, 0]), int(pedestrians[i, 1])] += 1.0 #Adds plus one at location of the all pedestrians 
    if j % 10 == 0: # saves trail image every 10 iterations
        plt.imsave(path.join(newpath, "State_{0}.png".format(pic_number)), G_akt)  # saves image at location 'newpath'
        pic_number = pic_number + 1  
    if j % 100 == 0: # saves absolulte/normalized trail image every 100 iterations
        print ("Saved Picture")
        Pedestrianrecordnorm = Pedestrianrecord / (np.amax(Pedestrianrecord))
        plt.imsave(path.join(newpath, "Pedcontroll_norm_{0}.png".format(j)),Pedestrianrecordnorm)  # save normalized trail image
        Pedestrianrecordnorm = np.clip(Pedestrianrecord, 0, 1)
        plt.imsave(path.join(newpath, "Pedcontroll_clip_{0}.png".format(j)),Pedestrianrecordnorm) # save absolute trail image
end = timeit.timeit()
print ("Time used for calculation: ",end-start,"[s]")
##############################################################################
##############################################################################