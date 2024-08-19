# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 09:10:27 2024

@author: zoech
"""

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

#"C:\Users\zoech\Desktop\Jacks Reserach 2024\Code\HI Code\7-7-24 fabric 5.txt"
#r"C:\Users\zoech\Downloads\7-24-24 spring test 4.txt"
#"C:\Users\zoech\Downloads\7-24-24 spring test 1.txt"
# "C:\Users\zoech\Desktop\Jacks Reserach 2024\Code\Working Code - Testing Stuff Out!\non-looping spring.txt"

''' input file path '''

input_file_path = r"C:\Users\zoech\Desktop\Jacks Reserach 2024\Code\Working Code - Testing Stuff Out!\non-looping spring.txt"
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
            

            # Check if the direction changed from down to up, indicating the start of a new loop
            if previous_direction == "up" and direc == "down" and current_loop['x']:
                loops.append(current_loop)
                
                # Start the new loop with the last data point from the previous loop
                current_loop = {'x': [current_loop['x'][-1]], 'y': [current_loop['y'][-1]]}
            else:
                current_loop['x'].append(disp/40)
                current_loop['y'].append(float(ws[0])*0.00981)
            
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



# Labeling axes and title

# manually setting x and y axes
# plt.xlim(7,8) 
# plt.ylim(0.125,0.275)


print(calibrated_ws)
print(pulse_disps)
print(len(calibrated_ws)== len(pulse_disps))

i = 0
downs = []
ups = []
while i < len(loops):
    xs = loops[i]['x']
    ys = loops[i]['y']
    
    half = int(len(ys)/2)-1
    
    downs.append(ys[:half])
    ups.append(ys[half+1:])
    i +=1
       
downs_array = np.array(downs)

# Step 1: Calculate the mean for each position
means = np.mean(downs_array, axis=0)

# Step 2: Calculate the squared differences from the mean
squared_diffs = (downs_array - means) ** 2

# Step 3: Calculate the variance at each position (x-value index)
variances = np.mean(squared_diffs, axis=0)

# Step 4: Calculate SE at each position
SEs = np.sqrt(variances) / np.sqrt(len(loops))

print("Variances at each x-value in DOWN direction:", variances)
print("Standard Error at each x-value in DOWN direction:", SEs)
# Plot each loop with a different color

ups_array = np.array(ups)

# Step 1: Calculate the mean for each position
means = np.mean(ups_array, axis=0)

# Step 2: Calculate the squared differences from the mean
squared_diffs = (ups_array - means) ** 2

# Step 3: Calculate the variance at each position (x-value index)
variances = np.mean(squared_diffs, axis=0)

# Step 4: Calculate SE at each position
SEs = np.sqrt(variances) / np.sqrt(len(loops))

print("Variances at each x-value in UP direction:", variances)
print("Standard Error at each x-value in UP direction:", SEs)

label = input("Spring or Fabric?: ") 

plt.xlabel('Displacement (cm)', fontsize=20)
plt.ylabel('Applied Force (N)', fontsize=20)
plt.title('Applied Force vs. Displacement with '+label, fontsize=20, fontweight='bold')
plt.legend()
plt.show()