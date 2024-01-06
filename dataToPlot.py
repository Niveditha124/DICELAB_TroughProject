import re
import numpy as np
import os
import sys
import time
from datetime import datetime
from os import listdir
from os.path import isfile, join
import plotGenerator
from serializer import Serializer

# Define a function to extract the numeric part from the filename
def extract_numeric_part(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else -1

# TODO: Get datasource folder from user however tf you want idc at this point <3
# Get the parent folder: eg: 2023_10_25_19_00_00
# dataSource = 'my_folder_2023_10_29_00_09_55'
dataSource = input('Please enter the folder of a run: ')

# Parse in filed object

try:
    # Get all field txt files
    dataFiles = [f for f in os.listdir(join(dataSource, 'serialized'))]
    # Sort them in order so it makes sense
    sorted_dataFiles = sorted(dataFiles, key=extract_numeric_part)
except:
    print('Please ensure that you have fieldX.txt files at the given directory (dataSource)')
    print(dataSource)
    sys.exit()


folder_flowprofile = os.path.join(dataSource, os.path.join('images', 'flowprofile'))
folder_iacbchanges = os.path.join(dataSource, os.path.join('images', 'iacbchanges'))
folder_kfrprofile = os.path.join(dataSource, os.path.join('images', 'kfrprofile'))
folder_ucprofike = os.path.join(dataSource, os.path.join('images', 'ucprofile'))

print()

for file in sorted_dataFiles:

    filename = os.path.join(dataSource, os.path.join('serialized', file))
    # Using our personally created serializer class
    serializerObj = Serializer.decode(filename)
    field, field_0, field_prev, par, dt = serializerObj.field, serializerObj.field_0, serializerObj.field_prev, serializerObj.par, serializerObj.dt
    import re
    pattern = r"field(\d+)\.txt"
    match = re.search(pattern, file)
    if match:
        titleCounter = int(match.group(1))
    else:
        print('Cannot find a file with the appropriate name. Please try again')
        sys.exit()
    
    plotGenerator.generate_flowprofile(field, field_0, folder_flowprofile + '/plot' + str(titleCounter) + '.png')
    plotGenerator.generate_ucprofile(field, folder_iacbchanges + '/plot' + str(titleCounter) + '.png')
    plotGenerator.generate_kfrprofile(field, par, folder_kfrprofile + '/plot' + str(titleCounter) + '.png')
    plotGenerator.generate_iacbchanges(field, field_prev, field_0, dt, folder_ucprofike + '/plot' + str(titleCounter) + '.png')
    #TODO temp remove later
    print(file + ' plot created')

dataSource = os.path.join(dataSource, 'images')
print('Plots created successfully. Stored in ' + dataSource)