import numpy as np
from RK5_complex import RK5_c
import os
import time

# Saves in an unique archive .npy
def save_file(base_filename, data, counter):
    folder = "Data"
    os.makedirs(folder, exist_ok=True)  # Create the directory
    filename = os.path.join(folder, f"{base_filename}_{counter}.npy")
    np.save(filename, data)


#Takes from a 3D array one section and calculates the derivative
def der_pos_vel(x,t,M):
    np.seterr(divide='ignore', invalid='ignore')    
    G = 6.674E-11
    r = x[0:2,:]
    v = x[2:5,:]
    
    der_r = v
    der_v = np.zeros(der_r.shape, dtype=complex)
    
    for i in np.arange(0,5):
        r_body = r[:,i]
        d = -r[:,0:5]+r_body[:,np.newaxis]
        norm_d = np.linalg.norm(d, axis=0)**3
        norm_d = np.where(norm_d == 0, np.inf, norm_d)
        der_v[:, i] = np.sum(-G * M[0:5] / norm_d * d, axis=1)
        
    return np.vstack((der_r,der_v))



start_time=time.time()

dt = 120
t_fin = 3600*24*365*5
t0 = 0
t = np.arange(t0,t_fin,dt)
N = len(t)

G = 6.674E-11

M = np.array([1.89813E27, 8.94E22, 4.80E22, 1.482E23, 1.075E23], dtype=complex) #Jupiter, Io, Europe, Ganymede, Callisto

#Define the vector. The first index is the time. The second index are the positions and the velocities. The third is the body.
x = np.empty((1,4,(len(M))), dtype=complex)
x[0,:,0] = np.array([0,0,0,0]) #Jupiter
x[0,:,1] = np.array([4.216E8,0,0,np.sqrt(G*M[0]/4.216E8)]) #Io
x[0,:,2] = np.array([6.709E8,0,0,np.sqrt(G*M[0]/6.709E8)]) #Europe
x[0,:,3] = np.array([1.07E9,0,0,np.sqrt(G*M[0]/1.07E9)]) #Ganymede
x[0,:,4] = np.array([1.883E9,0,0,np.sqrt(G*M[0]/1.883E9)]) #Callisto



t = np.arange(t0,t_fin,dt)


counter = 1
print("It is going to be created " + str(np.floor(N/10000)) + " files")
for i in np.arange(1,N):
    x = np.concatenate((x,RK5_c(der_pos_vel,np.squeeze(x[-1:,:,:]),t[i],dt,M)[np.newaxis,:,:]),axis = 0)

    if x.shape[0] >= 10000:
        # Convert the array to a NumPy format.
        np_x = np.real(np.array(x[:-1,:,:]))  # All except the last one
        # Save with an unique name
        save_file("Jup", (np_x).real.astype(np.float64), counter)
        print("File "+ str(counter) + " has been created")
        counter += 1  # Increase the counter
        # Hold only the last one element
        x = x[-1:,:,:]

end_time = time.time()

print("It has taken " + (end_time-start_time) + " seconds")
