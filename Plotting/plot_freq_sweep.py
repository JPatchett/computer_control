#################################################
#################################################
###### Live Plotting of a frequency sweep #######
#################################################
#################################################

#################################################
############### James Patchett ##################
################## 14/03/19 #####################
#################################################

## Set up the animation function for live plotting
## Set up the animation function for live plotting

#Data handling imports
import numpy as np
import pandas as pd

#Plotting imports
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Import imports
import glob
import os

#Misc imports
import time

#Make the plot live-update in the notebook
#Remove this command if not using Jupyter-Notebook

#Directory to scan for files in
directory_addr = r'C:\Data\James\Data\SP75A2\FMR\11.03.19\\'

#Data handling imports
import numpy as np
import pandas as pd

#Plotting imports
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Import imports
import glob
import os

#Misc imports
import time

#Make the plot live-update in the notebook
#Remove this command if not using Jupyter-Notebook

#Variable for saving plots
previous_file = 0

def animate(i, directory_addr, ax): 
    files = glob.glob(directory_addr+"*.csv")

    latest_file = max(files, key = os.path.getmtime)
    
    if previous_file == 0:
        previous_file = latest_file
    elif previous_file != latest_file:
        try:
            plt.savefig(os.path.splitext(os.path.basename(latest_file))[0]+".png")
        except Exception:
            print(Exception)
            
    try:
        data = pd.read_csv(latest_file)
    except:
        data = 0

    ax.clear()
    ax.set_xlabel("Frequency \\GHz")
    ax.set_ylabel("Magnetic Field \\uV")
    try:
        ax.imshow(data['Magnetic Field \T'], data['Output voltage \V']*1e6)
    except:
        pass

    previous_file = latest_file


#Animate the graph, check for updates every 1 second
def single_freq_animation(directory_addr):
    #Create a figure
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    an = animation.FuncAnimation(fig, animate, interval = 1000, fargs = (directory_addr, ax))
    plt.show()

directory_addr = r'C:\Data\James\Data\SP75A2\FMR\14.03.19\\'
single_freq_animation(directory_addr)