import re
import numpy as np
import os
import sys
import time
from datetime import datetime
from os import listdir
from os.path import isfile, join
import plotGenerator
import serializer

# Define a function to extract the numeric part from the filename
def extract_numeric_part(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else -1

# Path to directory containing data files (field0.txt, field1.txt, etc.)
dataSource = './data'
plotOutputFolder = ''
plotFolders = ['flowprofile', 'iacbchanges', 'kfrprofile', 'ucprofile']

# Parse in field object information into field object
# Done using jsonpickle

# Run field objects through plotGenerator and output plots to plotOutputFolder



# Parse in filed object

try:
    # Get all field txt files
    dataFiles = [f for f in os.listdir(dataSource) if isfile(join(dataSource, f))]
    # Sort them in order so it makes sense
    sorted_dataFiles = sorted(dataFiles, key=extract_numeric_part)
except:
    print('Please ensure that you have fieldX.txt files at the given directory (dataSource)')
    sys.exit()

# Filenames of all fieldX.txt files
print(sorted_dataFiles)

# Creates output at a folder with a timestamp

if not os.path.exists(plotOutputFolder):
    plotOutputFolder = './' + plotOutputFolder + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.mkdir(plotOutputFolder)

    for subfolder in plotFolders:
        os.mkdir(plotOutputFolder + '/' + subfolder)
    
# Call generators

for file in sorted_dataFiles:
    filename = plotOutputFolder + '/' + file
    # Using our personally created serializer class
    field = serializer.decode(filename)
    plotGenerator.generate_flowprofile(field, field_0, titleCounter)
    plotGenerator.generate_ucprofile(field, titleCounter)
    plotGenerator.generate_kfrprofile(field, par, titleCounter)
    plotGenerator.generate_iacbchanges(field, field_prev, field_0, dt, titleCounter)

