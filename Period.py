import numpy as np
import matplotlib.pyplot as plt
import os
import time

#Object that saves when a moon goes through its periapsis
class Moon:
    def __init__(self):
        self.periapsis = []  #Start with a empty list

    def add_element(self, elemento):
        self.periapsis.append(elemento)  # Add an element to the array

    def show_variable(self):
        return self.periapsis  # Give the array


# Function to obtain the data from three differents times
def obtener_datos(frame):

    # Initialize variables
    last_data = None
    current_data = None
    subsequent_data = None
    
    # Finding in which archive we are
    frames_accumulated = 0
    current_archive_idx = None
    frame_archive = None

    for i, num_frames in enumerate(size_archive):
        if frames_accumulated + num_frames > frame:
            current_archive_idx = i
            frame_archive = frame - frames_accumulated
            break
        frames_accumulated += num_frames

    # If we don't find the frame, return None
    if current_archive_idx is None:
        return None, None, None



    # Seeing the frames
    current_path = os.path.join(directory, archive[current_archive_idx])
    x = np.load(current_path)
    current_data = np.real(x[frame_archive, :, :])  # Current data
    
    # Data from the last frame
    if frame_archive > 0:
        last_data = np.real(x[frame_archive - 1, :, :])
    elif current_archive_idx > 0:
        # Load the last one frame of the last archive
        last_route = os.path.join(directory, archive[current_archive_idx - 1])
        last_x = np.load(last_route)
        last_data = np.real(last_x[-1, :, :])
    else:
        last_data = None

    # Data from the subsequent frame
    if frame_archive < x.shape[0] - 1:
        subsequent_data = np.real(x[frame_archive + 1, :, :])
    elif current_archive_idx < len(archive) - 1:
        print("Finish "+archive[current_archive_idx])
        # Load the first frame of the subsequent archive
        subsequent_route = os.path.join(directory, archive[current_archive_idx + 1])
        subsequent_x = np.load(subsequent_route)
        subsequent_data = np.real(subsequent_x[0, :, :])
    else:
        subsequent_data = None
                
    return last_data, current_data, subsequent_data


# directory where there are .npy archives
directory = '.' 

# Obtain the arhives that start with 'Jup_' and end with '.npy'
archive = sorted(
    [f for f in os.listdir(directory) if f.startswith('Jup_') and f.endswith('.npy')],
    key=lambda f: int(f.split('_')[1].split('.')[0])  # Extrac the number to order
)

#See the first archive to know the number of bodys
x = np.load("Jup_1.npy")
num_bodys = x.shape[2]  # Number of bodys

# Create a list of moons
moons = [Moon() for _ in range(num_bodys-1)]  # List with all the moons

# Total number of frames
total_frames = sum(np.load(os.path.join(directory, archive)).shape[0] for archive in archive)

# Index the archives and their sizes
size_archive = []
for archive in archive:
    route = os.path.join(directory, archive)
    x = np.load(route, mmap_mode='r')  # Use mmap_mode for not load all the information at the same time (faster)
    size_archive.append(x.shape[0])  # Number of frames in each archive


#Find the period seeing the periapsis
periapsis_times = []

for i in np.arange(1,total_frames-1):
    x0, x1, x2 = obtener_datos(i)
    r0, r1, r2 = np.sqrt((x0[0,1:]-x0[0,0])**2+(x0[1,1:]-x0[1,0])**2),np.sqrt((x1[0,1:]-x1[0,0])**2+(x1[1,1:]-x1[1,0])**2),np.sqrt((x2[0,1:]-x2[0,0])**2+(x2[1,1:]-x2[1,0])**2)
    counter = 0
    for moon in moons:
        if r1[counter] < r0[counter] and r1[counter] < r2[counter]:  # Periapsis crossing
            moon.add_element(i)
        counter += 1
            
# Save the moons array in a .npy archive
np.save("Periapsis.npy", moons, allow_pickle=True)
