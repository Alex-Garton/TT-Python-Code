# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 09:31:09 2024

@author: zoech
"""
# This is the required script for checking the linearity of vertical displacement
    # to number of steps. 

# Required libraries
import os
import matplotlib.pyplot as plt
import numpy as np
import re

''' input file path '''

input_file_path = r"C:\Users\zoech\Downloads\7-12-24 pulse-displacement calibration 3.txt"

# Patterns used to extract values and initialized empty lists
decimal_pattern = r"-?\d+\.\d+"
int_pattern = r'-?\d+'
steps = []
disps = []


''' reading the input file '''

with open(input_file_path, 'r') as file:
    for line in file:
        line = line.strip()
        
        if "steps" in line:
            steps.append(int(re.search(int_pattern, line).group()))
            
        elif "displacement" in line:
            disps.append(float(re.search(decimal_pattern, line).group()))

x = steps
y = disps

# Plotting the points
plt.plot(x, y, 'o', label='Data points')
 
# Fitting a linear regression line
coefficients = np.polyfit(x, y, 1)
poly = np.poly1d(coefficients)
y_fit = poly(x)
 
#P lotting the line of best fit
plt.plot(x, y_fit, label=f'Line of best fit: y = {coefficients[0]:.5f}x + {coefficients[1]:.2f}', color='red')
 
# Calculating residuals and standard deviation
residuals = y - y_fit
std_dev = np.std(residuals)
 
# Calculating correlation coefficient (r)
correlation_matrix = np.corrcoef(x, y)
correlation_coefficient = correlation_matrix[0, 1]
 
# Adding standard deviation and correlation coefficient information to the plot
plt.text(0.95, 0.05, f'Standard Deviation: {std_dev:.2f}\nCorrelation Coefficient (r): {correlation_coefficient:.2f}', 
         horizontalalignment='right', verticalalignment='bottom', transform=plt.gca().transAxes,
         bbox=dict(facecolor='yellow', alpha=0.5))

# Labeling axes and title
plt.xlabel('Number of Steps')
plt.ylabel('Displacement (cm)')
plt.title('Pulse Displacement Calibration')
plt.legend()
 
# Showing the plot
plt.show()
 
 
