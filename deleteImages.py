'''
    Deletes all plot images made in the images folder
    Feel free to change this code as per whatever you want idc.
    Note: Now also deletes serialized folder content
'''

import os
 
root_dir = 'images/python/'
# Folders containing images of the 4 graphs.
dir = ['flowprofile', 'iacbchanges', 'kfrprofile', 'ucprofile']
for directories in dir:
    for f in os.listdir(os.path.join(root_dir, directories)):
        os.remove(os.path.join(os.path.join(root_dir, directories), f))

deleteDataFlag = input('Would you also like to delete data files? (y/n)')

if deleteDataFlag.strip().lower() == 'y':
    for f in os.listdir('./data'):
        os.remove('./data/' + str(f))
    for f in os.listdir('./serialized'):
        os.remove('./serialized/' + str(f))

    print('All plots and data files deleted')

else: print('ONLY plots deleted')