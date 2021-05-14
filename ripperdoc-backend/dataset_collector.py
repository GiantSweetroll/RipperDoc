import shutil
import os

def process_flickr27(logos_to_find: list, dst_folder:str):
    root_directory : str = "L:/For Machine Learning/Logo Recognition/flickr_logos_27_dataset/flickr_logos_27_dataset/"      # The root directory of where to get the files
    images_source_directory: str = root_directory + 'flickr_logos_27_dataset_images/'    # Location of the original images

    # Scan through the training dataset and only extract the images that matches the category
    included_data_train: list = []        # list that stores the matching data
    training_file = open(root_directory + "flickr_logos_27_dataset_training_set_annotation.txt")     #Load the training dataset file
    for x in training_file.read().splitlines():
        for logo in logos_to_find:
            sub:list = x.split()
            if sub[1] == logo:
                included_data_train.append(x)
                src_path:str = images_source_directory + sub[0]
                dst_path:str = dst_folder + sub[1] + "/"
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path)
                shutil.copy2(src_path, dst_path + sub[0])      # Copy image to new directory

    # Scan through the query dataset and only extract the images that matches the category
    included_data_validation : list = []
    validation_file = open(root_directory + "flickr_logos_27_dataset_query_set_annotation.txt") #Load the query dataset file
    for x in validation_file.read().splitlines():
        for logo in logos_to_find:
            sub:list = x.split()
            if sub[1] == logo:
                included_data_validation.append(x)
                src_path:str = images_source_directory + sub[0]
                dst_path:str = dst_folder + sub[1] + "/"
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path)
                shutil.copy2(src_path, dst_path + sub[0])      # Copy image to new directory

    # Write to file
    trimmed_train_dataset = open(root_directory + "trimmed_training_dataset.txt", "w")
    for x in included_data_train:
        trimmed_train_dataset.write(x + "\n")

    trimmed_query_dataset = open(root_directory + "trimmed_validation_dataset.txt", "w")
    for x in included_data_validation:
        trimmed_query_dataset.write(x + "\n")

def process_flickr32plus(logos_to_find: list, dst_folder:str):
    src_folder:str = 'L:/For Machine Learning/Logo Recognition/Flickr32_Plus/images/'       # Location of original dataset

    # Loop through logo and find existing folders
    for logo in logos_to_find:
        path:str = src_folder + logo + "/"
        
        if os.path.exists(path):
            shutil.copytree(src=path, dst=dst_folder + logo + "/", dirs_exist_ok = True)

ripperdoc_dataset_folder: str = 'L:/For Machine Learning/Project/RipperDoc/dataset/'         # Location of filetered images

# Process what category to find
logo_to_find_file = open("documents/logos", "r")    # load the file that contains what logo to find from the training datasets
logos_to_find: list = logo_to_find_file.read().splitlines()    # Variable to store the string of what logos to look for
print("Logos to find:", logos_to_find)

# Filter dataset
print("Filtering Flickr27 dataset...")
process_flickr27(logos_to_find, ripperdoc_dataset_folder)
print("Filtering Flickr32Plus dataset...")
process_flickr32plus(logos_to_find, ripperdoc_dataset_folder)
print("Done!")