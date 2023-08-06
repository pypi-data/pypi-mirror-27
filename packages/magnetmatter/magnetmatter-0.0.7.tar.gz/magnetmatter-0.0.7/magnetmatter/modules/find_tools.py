# find.py

import os

def findfile(extension):
    """ returns only one file with extension """
    files = [f for f in os.listdir() if f.endswith(extension)]
    searched_file = files[0] if len(files)==1 else "error!"
    if searched_file == "error!":
        print("error finding file with extension:", extension, "in folder", os.getcwd())
        print("number of files with extension:", len(files))
    #     import pdb; pdb.set_trace()
    # else:
    return searched_file

def findfiles(extension):
    """ returns all files with specified extension """
    return [f for f in os.listdir() if f.endswith(extension)]

def findfolders():
    """ returns all folders in cwd """
    return [f for f in os.listdir() if os.path.isdir(f)]
