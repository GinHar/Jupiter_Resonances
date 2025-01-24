import numpy as np
import os
import matplotlib.pyplot as plt



# Directory where there are .npy archives
directory = 'Data' 

# Obtain the arhives that start with 'Jup_' and end with '.npy'
archive = sorted(
    [f for f in os.listdir(directory) if f.startswith('Jup_') and f.endswith('.npy')],
    key=lambda f: int(f.split('_')[1].split('.')[0])  # Extrac the number to order
)

# Obtaining the frequencies
max_frequencies = []
for archive in archives:
    x = np.load(archive) #Load each archive
    r = np.sqrt((x[:, 0, 1:] - x[:, 0, 0:1])**2 + (x[:, 1, 1:] - x[:, 1, 0:1])**2) # Distance between Jupyter and his moons
    
    # FFT
    r_fft = np.fft.rfft(r,axis=0)
    magnitudes = np.abs(r_fft)
    # Maximun value
    magnitudes = np.abs(r_fft)[1:]  # We don't want the constant value

    # Find the index where the maximun value is
    max_index = np.argmax(magnitudes, axis=0) + 1  # Plus 1 because we have ignored the constant value

    
    # Frequencies
    frequencies = np.fft.rfftfreq(r.shape[0], 120)
    #The maximun frecuency
    max_frequencies.append(np.take(frequencies, max_index))
    print(archive + " has been analyzed")

# Plotting the period
periods = 1/np.array(max_frequencies)/3600/24 #Period in days
x = np.arange(1, periods.shape[0] + 1)  # [1, 2, 3, 4, 5]

for i in range(periods.shape[1]):
    plt.plot(x, periods[:, i], marker='o', markersize=1)

plt.ylim(0,14)
plt.ylabel("Period (days)")
plt.xlabel("Each file (One tick is around 14 days)")
plt.legend(["Io", "Europe", "Ganymedes", "Callisto"])
plt.title("Periods of the Jupyter's moons")
plt.show()
