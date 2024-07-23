# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 1:55:49 2024

@author: zoech
"""
# This script will be used to show trends when plotting TT weight (g) measurements
    # at different vertical displacements. Currently, pulse displacement describes
    # how far the force sensor-bearing arm moves down and up from where it is
    # tared (0).

# Required libraries
import os
import matplotlib.pyplot as plt
import numpy as np
import re

''' input file path '''

input_file_path = 

# Initialize lists and variables
calibrated_ws = []
pulse_disps = []
disp = 0
decimal_pattern = r"-?\d+\.\d+"
int_pattern = r'-?\d+'
loops = []  # To store each loop data
current_loop = {'x': [], 'y': []}
previous_direction = None  # To track the previous direction


''' reading the input file '''

# Read the data
    # Goes through input file and parses information by category. First, the 
    # Calibration Factor is saved as cf. Then, we extract the step size and
    # calibrated weights. We save the direction and increment step size based
    # off of whether we are traveling up or down. One loop is defined as one
    # cycle of going down, then up.  
    
with open(input_file_path, 'r') as file:
    for line in file:
        line = line.strip()
        
        if "calibration factor" in line:
            cf = int(re.search(int_pattern, line).group())
            print("Calibration Factor:", cf)
            
        elif line.startswith('| step size:'):
            step_size = int(re.search(int_pattern, line).group())
            
            if "up" in line:
                direc = "up"
            else:
                direc = "down"

        elif line.startswith('| one reading:'):
            ws = re.findall(decimal_pattern, line)
            calibrated_ws.extend([float(w) for w in ws])
            
            if direc == "up":
                disp -= step_size
            else:
                disp += step_size
            
            pulse_disps.append(disp)
            current_loop['x'].append(disp)
            current_loop['y'].append(float(ws[0]))

            # Check if the direction changed from down to up, indicating the start of a new loop
            if previous_direction == "up" and direc == "down" and current_loop['x']:
                loops.append(current_loop)
                current_loop = {'x': [], 'y': []}

            previous_direction = direc

# Add the last loop if it's not empty
if current_loop['x']:
    loops.append(current_loop)


''' plotting '''

# Plot each loop with a different color
plt.figure(figsize=(10, 6))
colors = plt.cm.viridis(np.linspace(0, 1, len(loops)))

for i, loop in enumerate(loops):
    plt.plot(loop['x'], loop['y'], 'o-', label=f'Loop {i+1}', linewidth=1, markersize=2, color=colors[i])

# Add an arrow for "Up"
plt.annotate('Up', xy=(0.75, 0.3), xycoords='axes fraction',
             xytext=(0.9, 0.5), textcoords='axes fraction',
             arrowprops=dict(facecolor='green', shrink=0.05, width=1.5),
             horizontalalignment='right')

# Add an arrow for "Down"
plt.annotate('Down', xy=(0.25, 0.45), xycoords='axes fraction',
             xytext=(0.1, 0.3), textcoords='axes fraction',
             arrowprops=dict(facecolor='red', shrink=0.05, width=1.5),
             horizontalalignment='left')

# Labeling axes and title
plt.xlabel('Pulse Displacement')
plt.ylabel('TT Weight (g)')
plt.title('Pulse Displacement vs. TT Weight')
plt.legend()
plt.show()

