import numpy as np
import matplotlib.pyplot as plt
import os
import time

#Creo un objeto que guardara cuando ocurre la periapsis en cada satelite
class Satelite:
    def __init__(self):
        self.periapsis = []  # Inicializamos como una lista vacía

    def agregar_elemento(self, elemento):
        self.periapsis.append(elemento)  # Agrega un elemento al array

    def mostrar_variable(self):
        return self.periapsis  # Devuelve el contenido de la lista


# Función para obtener los datos de tres fotogramas: anterior, actual y posterior
def obtener_datos(frame):
       
    frames_restantes = frame
    # Inicializar las variables para los fotogramas
    datos_anterior = None
    datos_actual = None
    datos_posterior = None
    
    # Determinar en qué archivo se encuentra el fotograma actual
    frames_acumulados = 0
    archivo_actual_idx = None
    frame_en_archivo = None

    for i, num_frames in enumerate(tamanos_archivos):
        if frames_acumulados + num_frames > frame:
            archivo_actual_idx = i
            frame_en_archivo = frame - frames_acumulados
            break
        frames_acumulados += num_frames

    # Si no se encuentra el fotograma, retornamos None
    if archivo_actual_idx is None:
        return None, None, None



    # Acceder al fotograma anterior, actual y posterior
    ruta_actual = os.path.join(directorio, archivos[archivo_actual_idx])
    x = np.load(ruta_actual)
    datos_actual = np.real(x[frame_en_archivo, :, :])  # Datos del fotograma actual
    
    # Datos del fotograma anterior
    if frame_en_archivo > 0:
        datos_anterior = np.real(x[frame_en_archivo - 1, :, :])
    elif archivo_actual_idx > 0:
        # Cargar último fotograma del archivo anterior
        ruta_anterior = os.path.join(directorio, archivos[archivo_actual_idx - 1])
        x_anterior = np.load(ruta_anterior)
        datos_anterior = np.real(x_anterior[-1, :, :])
    else:
        datos_anterior = None

    # Datos del fotograma posterior
    if frame_en_archivo < x.shape[0] - 1:
        datos_posterior = np.real(x[frame_en_archivo + 1, :, :])
    elif archivo_actual_idx < len(archivos) - 1:
        print("Termina"+archivos[archivo_actual_idx])
        # Cargar primer fotograma del archivo posterior
        ruta_posterior = os.path.join(directorio, archivos[archivo_actual_idx + 1])
        x_posterior = np.load(ruta_posterior)
        datos_posterior = np.real(x_posterior[0, :, :])
    else:
        datos_posterior = None
                
    return datos_anterior, datos_actual, datos_posterior


# Directorio donde están los archivos .npy
directorio = '.'  # Ajusta el directorio si no está en el directorio actual

# Obtener los archivos que empiezan con 'Jup_' y terminan con '.npy'
archivos = sorted(
    [f for f in os.listdir(directorio) if f.startswith('Jup_') and f.endswith('.npy')],
    key=lambda f: int(f.split('_')[1].split('.')[0])  # Extrae el número para ordenar
)

#Miro los datos del primer archivo para conocer el número de partículas
x = np.load("Jup_1.npy")
num_particulas = x.shape[2]  # Número total de partículas

# Crear un array (lista) de satelites
satelites = [Satelite() for _ in range(num_particulas-1)]  # Lista con todos los satelites

#El dt
dt = 1

# Calcular el número total de instantes de tiempo
total_frames = sum(np.load(os.path.join(directorio, archivo)).shape[0] for archivo in archivos)

# Indexar los archivos y sus tamaños
tamanos_archivos = []
for archivo in archivos:
    ruta = os.path.join(directorio, archivo)
    x = np.load(ruta, mmap_mode='r')  # Usar mmap_mode para no cargar todo en memoria
    tamanos_archivos.append(x.shape[0])  # Número de fotogramas en cada archivo


#Hallo el periodo fijandome en la periapsis
periapsis_times = []

for i in np.arange(1,total_frames-1):
    x0, x1, x2 = obtener_datos(i)
    r0, r1, r2 = np.sqrt((x0[0,1:]-x0[0,0])**2+(x0[1,1:]-x0[1,0])**2),np.sqrt((x1[0,1:]-x1[0,0])**2+(x1[1,1:]-x1[1,0])**2),np.sqrt((x2[0,1:]-x2[0,0])**2+(x2[1,1:]-x2[1,0])**2)
    counter = 0
    for satelite in satelites:
        if r1[counter] < r0[counter] and r1[counter] < r2[counter]:  # Periapsis crossing
            satelite.agregar_elemento(i)
        counter += 1
            
# Guardar el array de objetos en un archivo .npy
np.save("Periapsis.npy", satelites, allow_pickle=True)

period = np.diff(satelites[1].mostrar_variable())
x = np.arange(0,len(period))
plt.figure(1)
plt.plot(x,period,'o')
