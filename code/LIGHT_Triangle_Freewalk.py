import numpy as np
import matplotlib.pyplot as plt
import random

##############################################################################
# To Do: Install NUMPY and MATPLOTLIB library
##############################################################################

##############################################################################
## Parameters for run
## Choose your parameter in the sequence of parameter
iterations = 500  # amount of cycles
Intensity = 0.35  # Destruction of Trail (I)
Durability = 250  # Growth rate / regeneration (T) The higher, the slower the grass grows
sigma = 4  # Visibility
v0 = 1  # Velocity of pedestrian
ped_num = 6  # Number of Pedestrians
##############################################################################

         
##############################################################################
field = [30, 30]  # field area
G_0 = np.asarray(np.zeros((field[0], field[1]), dtype=float))  # ground structure
G_akt = np.asarray(np.zeros((field[0], field[1]), dtype=float))  # actual ground structure
G_max = np.asarray(np.ones((field[0], field[1]), dtype=float))  # max of ground structure
pedestrians = np.ones((ped_num, 4)) # Array where the start-x, start-y, destination-x und destination-y position of pedestrian are saved
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
        g_ak[x, y] = d_g[x, y] + g_ak[x, y] # Update of actual ground structure
    return g_ak
##############################################################################
    

##############################################################################
## Function calculates trail potential
##
## Inputs: x and y position to calculate trail potential; Sigma (Visibility); G_akt (actual field structure),
## Outputs: vtr (trail potential)
def d_r(x, y, G_ak, sig):
    vtr = 0
    for i in range(0, field[0]):
        for k in range(0, field[1]):
            dist = np.sqrt((i - x) ** 2 + (k - y) ** 2) # distance calculation for trail potential
            vtr = vtr + np.exp(-dist / sig) * G_ak[i, k] # trail potential calculation
    vtr = vtr/(field[0]*field[1])
    return vtr
##############################################################################


##############################################################################
##Function calculates derivation of trail potential and vector to destination of pedestrian 
##
## Inputs: pedestrian ; Sigma (Visibility); G_akt (actual field structure)
## Outputs: derivation of vtr (trail potential) in vertical direction
def vec(ped, G_ak, sig):
    dVtr = np.asarray(np.zeros((ped.shape[0], 2), dtype=float))
    d_dest = np.asarray(np.zeros((ped.shape[0], 2), dtype=float))
    for i in range(0, ped.shape[0]):
        x = int(round(ped[i, 0]))
        y = int(round(ped[i, 1]))
        Vtr1 = d_r(x + 1, y, G_ak, sig) #calculates the trail potential
        Vtr2 = d_r(x, y + 1, G_ak, sig) #calculates the trail potential
        Vtr3 = d_r(x - 1, y, G_ak, sig) #calculates the trail potential
        Vtr4 = d_r(x, y - 1, G_ak, sig) #calculates the trail potential
        dVtr[i, 0] = (Vtr1 - Vtr3) / 2 #calculates derivation of trail potential in vertical direction
        dVtr[i, 1] = (Vtr2 - Vtr4) / 2 #calculates derivation of trail potential in horizontal direction
        d_dest[i, 0] = ped[i, 2] - ped[i, 0] #calculates vertical part of vector to destination of pedestrian 
        d_dest[i, 1] = ped[i, 3] - ped[i, 1] #calculates horizontel part of vector to destination of pedestrian 
    return {"d_dest": d_dest, "d_Vtr": dVtr}
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
        lengthl = np.sqrt((d_dest[i, 0] + dVtr[i, 0]) ** 2 + (d_dest[i, 1] + dVtr[i, 1]) ** 2)  #length of combined vector (destination + potential vector)
        epdest[i, 0] = (d_dest[i, 0] + dVtr[i, 0]) / (lengthl) * v0  # pedestrian vertical displacement vector
        epdest[i, 1] = (d_dest[i, 1] + dVtr[i, 1]) / (lengthl) * v0  # pedestrian horizontal displacement vector
    return epdest
##############################################################################
    

##############################################################################
## Function for respawning of the pedestrians when they reach their destination
## Attention respwan point are spezific for park
## Inputs:  pedestrian
## Outputs: pedestrian (updated pedestrian array)
def respawn(ped):
    for i in range(0, ped.shape[0]):
        p_0 = [[15, 2], [27,27],[2,27]] #respwan points specifig for park alcala
        if (abs(round(ped[i, 0]) - round(ped[i, 2]))) < 1.5 and abs(round(ped[i, 1]) - round(ped[i, 3])) < 1.5: #when pedestrian reach destination
            ped[i,0], ped[i,1] = random.choice(p_0) #random choice of location in p0 for start position
            ped[i,2], ped[i,3] = random.choice(p_0) #random choice of location in p0 for destination position
            while ((ped[i,0]== ped[i,2]) and (ped[i,1]== ped[i,3])): # prohibits that destination is equal to start
                ped[i,2], ped[i,3] = random.choice(p_0)
    return ped
##############################################################################


##############################################################################
# main from which all the functions are called
for j in range(0, iterations):
    print("Number of iterations: ", j+1, "/", iterations) # print current status of progress
    respawn(pedestrians) # respawn pedestrians that reched the destination
    G_akt = dG(Intensity, Durability, G_0, G_akt, G_max, pedestrians) # update the field matrix
    d_v = d_pos(pedestrians, G_akt, sigma, v0) # calculate walking direction of all pedestrians
    for i in range(0, pedestrians.shape[0]): # update the prositions of the pedestrians
        pedestrians[i, 0] = pedestrians[i, 0] + d_v[i, 0]
        pedestrians[i, 1] = pedestrians[i, 1] + d_v[i, 1]
        if j == (iterations-1):
            pedestrians[i, 0], pedestrians[i, 1] = [2,2]
plt.imshow(G_akt)
plt.show()
##############################################################################