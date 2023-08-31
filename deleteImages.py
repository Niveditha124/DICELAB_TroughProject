'''
    Deletes all plot images made in the images folder
    Feel free to change this code as per whatever you want idc.
'''

import os
 
root_dir = 'images/python/'
# Folders containing images of the 4 graphs.
dir = ['flowprofile', 'iacbchanges', 'kfrprofile', 'ucprofile']
for directories in dir:
    for f in os.listdir(os.path.join(root_dir, directories)):
        os.remove(os.path.join(os.path.join(root_dir, directories), f))