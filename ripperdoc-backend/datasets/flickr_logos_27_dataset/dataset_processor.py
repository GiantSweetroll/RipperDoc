import os as os

root_directory : str = "datasets/flickr_logos_27_dataset/"      # The root directory of where to get the files

# Process what category to find
logo_to_find_file = open(root_directory + "logo_to_find.txt", "r")    # load the file that contains what logo to find from the training datasets
logos_to_find: list = logo_to_find_file.read().splitlines()    # Variable to store the string of what logos to look for
print("Logos to find:", logos_to_find)

# Scan through the training dataset and only extract the images that matches the category
included_data_train: list = []        # list that stores the matching data
training_file = open(root_directory + "flickr_logos_27_dataset_training_set_annotation.txt")     #Load the training dataset file
for x in training_file.read().splitlines():
    for logo in logos_to_find:
        sub:list = x.split()
        if sub[1] == logo:
            included_data_train.append(x)

# Scan through the query dataset and only extract the images that matches the category
included_data_query : list = []
query_file = open(root_directory + "flickr_logos_27_dataset_query_set_annotation.txt") #Load the query dataset file
for x in query_file.read().splitlines():
    for logo in logos_to_find:
        sub:list = x.split()
        if sub[1] == logo:
            included_data_query.append(x)

# Write to file
trimmed_train_dataset = open(root_directory + "trimmed_training_dataset.txt", "w")
for x in included_data_train:
    trimmed_train_dataset.write(x + "\n")

trimmed_query_dataset = open(root_directory + "timmed_query_dataset.txt", "w")
for x in included_data_query:
    trimmed_query_dataset.write(x + "\n")