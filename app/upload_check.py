from app import app
from glob import glob
from valid_headers import *
import os
###
#The goal of this module is to make sure all the relevant files are uploaded before processing occurrs to generate the final output.
###

#To do: add all files to a database and then upload them there with timestamps, this will be helpful for data versioning as well as checks here.

#To do: remove data.csv

def remove_bad_files():
    upload_folder = app.config["UPLOAD_FOLDER"]
    current_files = glob(upload_folder+"/*")
    current_files_names = [f.split("/")[-1] for f in current_files] 
    all_files_needed = column_names.keys()
    name_loc = zip(current_files_names,current_files)
    for name,loc in name_loc:
        if not name in all_files_needed:
            os.remove(loc)
    
            
def check_for_all_files():
    upload_folder = app.config["UPLOAD_FOLDER"]
    current_files = glob(upload_folder+"/*")
    current_files = [f.split("/")[-1] for f in current_files]
    all_files_needed = column_names.keys()
    current_files.sort()
    all_files_needed.sort()
    if current_files == all_files_needed:
        return True # all files uploaded
    else:
        return False # some files missing
    
def get_missing_files():
    missing_files = []
    upload_folder = app.config["UPLOAD_FOLDER"]
    current_files = glob(upload_folder+"/*")
    current_files = [f.split("/")[-1] for f in current_files] 
    all_files_needed = column_names.keys()
    current_files.sort()
    all_files_needed.sort()
    if current_files != all_files_needed:
        for f in all_files_needed:
            if not f in current_files:
                missing_files.append(f)
    return missing_files
    
                
