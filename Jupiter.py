import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from RK_5_complex import RK5_c
from skyfield.api import load
import time

# Guardar cada segmento en un archivo .npy único
def save_to_unique_npy_file(base_filename, data, counter):
    filename = f"{base_filename}_{counter}.npy"
    np.save(filename, data)

#Coge de un array tridimensional un bloque y calcula la derivada de ese bloque
#Mi ordenador no aumenta la velocidad al paralelizar ni con la CPU ni con la GPU
#M es un array con la masas de los objetos
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

dt = 3600*24
t_fin = 3600*24*365*20000
t0 = 0
t = np.arange(t0,t_fin,dt)
N = len(t)

G = 6.674E-11

M = np.array([1.89813E27, 8.94E22, 4.80E22, 1.482E23, 1.075E23], dtype=complex) #Jupiter, Io, Europa, Ganimedes, Calisto

# Definir los cuerpos celestes que vas a observar
planets_list = ['Jupiter', 'Io', 'Europa', 'Ganymede', 'Callisto']



#Defino el vector
x = np.empty((1,4,(len(M))), dtype=complex)
x[0,:,0] = np.array([0,0,0,0]) #Jupiter
x[0,:,1] = np.array([4.216E8,0,0,np.sqrt(G*M[1]/4.216E8)]) #Io
x[0,:,2] = np.array([6.709E8,0,0,np.sqrt(G*M[2]/6.709E8)]) #Europa
x[0,:,3] = np.array([1.07E9,0,0,np.sqrt(G*M[3]/1.07E9)]) #Ganimedes
x[0,:,4] = np.array([1.883E9,0,0,np.sqrt(G*M[4]/1.883E9)]) #Callisto



t = np.arange(t0,t_fin,dt)


counter = 1
print(N/10000)
for i in np.arange(1,N):
    x = np.concatenate((x,RK5_c(der_pos_vel,np.squeeze(x[-1:,:,:]),t[i],dt,M)[np.newaxis,:,:]),axis = 0)

    if x.shape[0] >= 10000:
        print("Copia "+ str(counter))
        # Convierte el array a un formato NumPy
        np_x = np.real(np.array(x[:-1,:,:]))  # Todos menos el último
        # Guarda con un nombre único
        save_to_unique_npy_file("Jup", (np_x).real.astype(np.float64), counter)
        counter += 1  # Incrementa el contador
        # Mantén solo el último elemento
        x = x[-1:,:,:]




end_time = time.time()

print((end_time-start_time))