import sys
import matplotlib.pyplot as plt
import numpy as np

# Given data
data = [
    (1, 4.841470985),
    (5, 3.041075725),
    (20, 4.912945251),
    (50, 3.737625146),
    (100, 3.493634359),
    (200, 3.126702703),
    (250, 3.02947198),
    (260, 4.683239704),
    (300, 3.00024416),
    (500, 3.532228195),
    (750, 4.74507295),
    (850, 4.980227732),
    (1000, 4.826879541),
    (2000, 4.930039504),
    (3500, 4.262665725),
    (5000, 3.012033561),
    (5050, 3.006064849),
    (5100, 3.069739128),
    (5200, 3.383603427),
    (6000, 3.572280487),
    (6250, 3.019653152),
    (7000, 4.50688543),
    (7700, 4.043580142),
    (8500, 3.087350221),
    (10001, 3.033664726)
]

# # Init code for interpolation

# # initialise flow domain:
# n = 200
# x0 = 0 # (x0) defines the initial x-coordinate 
# Lx = 22000 # (Lx) repersents the length of the flow domain (1 m)
# y0 = 0 # (y0) defines the initial y-coordinate 
# Ly = 0.5 # (Ly) computes the total width of the flow domain (1 m) 
# dx = Lx/n # (dx) computes the grid spacing based off the sum of all reach lengths (Lx) and number of cells (n)
# dy=dx

# # creating an array of (x) values
# #x = (x0-0.5*dx):dx:(x0+Lx+0.5*dx)
# x = np.arange((x0-0.5*dx), (x0+Lx+0.5*dx) + 1, dx) # +1 to match MATLAB results

# #  setting field (x) and (y) attributes using the above arrays to define the grid
# fieldx = np.ones((1,1)) * x # field.x = np.ones(lengt(y), 1) * x


# # Extracting x and y coordinates
# xx = [point[0] for point in data]
# zz = [point[1] for point in data]
# z_b = np.ones(fieldx.shape) * -1000  # default
# z_b = np.interp(fieldx, xx, zz)
# z_b

# print(fieldx,z_b)
# plt.figure(1)
# plt.plot(xx, zz,linestyle='-', color='blue')
# plt.title('Original')

# plt.figure(2)
# plt.plot(fieldx[0], z_b[0])
# plt.title('Interpolated')

# plt.xlabel('X')
# plt.ylabel('Y')

# plt.show()

# print(fieldx.shape)

# # Plotting the data
# plt.plot(x, y, marker='o',linestyle='-', color='blue')

# # Adding labels and title
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Scatter Plot of Given Data')

# # Display the plot
# plt.show()























# Original data
x_original, y_original = zip(*data)

# Number of points you want after interpolation
desired_points = 202

# Interpolate to get additional points
x_interpolated = np.linspace(min(x_original), max(x_original), desired_points)
y_interpolated = np.interp(x_interpolated, x_original, y_original)

# Plot the original data
plt.plot(x_original, y_original, marker='o', linestyle='-', color='blue', label='Original')

# Plot the interpolated data
plt.plot(x_interpolated, y_interpolated, marker='x', linestyle='--', color='red', label='Interpolated')

# Adding labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Original and Interpolated Data')

# Add legend
plt.legend()

# Display the plot
plt.show()