import os
import shutil

src_folder:str = 'L:/For Machine Learning/Logo Recognition/Flickr32_Plus/images/'       # Location of original dataset
dst_folder:str = 'L:/For Machine Learning/Project/RipperDoc/dataset/'       # Location of filtered dataset

# Process what category to find
logo_to_find_file = open("documents/logos", "r")    # load the file that contains what logo to find from the training datasets
logos_to_find: list = logo_to_find_file.read().splitlines()    # Variable to store the string of what logos to look for
print("Logos to find:", logos_to_find)

# Loop through logo and find existing folders
for logo in logos_to_find:
    path:str = src_folder + logo + "/"
    
    if os.path.exists(path):
        shutil.copytree(src=path, dst=dst_folder + logo + "/", dirs_exist_ok = True)