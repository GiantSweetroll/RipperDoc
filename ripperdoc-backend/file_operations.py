import cv2
import glob
import pandas as pd
import constants

def load_image(filename):
    image = cv2.imread(filename)      # Read image file
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert from BGR to grayscale
    return image

def load_training_images(source:constants.Dataset = constants.Dataset.Flickr27) -> dict:
    """Get dictionary that maps the images for training"""
    # dataset_num = hsf folder number
    # data_size is the amount of data to be loaded, between 0 and 1. 1 means all of the data.
    images:{} = {}
    
    ### Load flickr_27 logos
    # Read training dataset file
    if source == constants.Dataset.Flickr27 or source == None:
        df: pd.DataFrame = pd.read_csv(constants.flickr_27_training_dataset_file, delimiter=' ', header=None)
        # Loop through data frame
        for i in df.index:
            image_file: str = df.loc[i][0]      # Image name
            label: str =  df.loc[i][1]          # Image label (what logo it is)
            image = load_image(constants.flickr_27_images_folder + image_file)      # Load the image into memory
            
            # Check if label exists in dictionary
            if images.get(label) != None:
                images[label].append(image)
            else:
                images[label] = [image]
    
    return images

def load_test_images(source:constants.Dataset = constants.Dataset.Flickr27):
    """A method to load the images used to test the neural network or for it to be predicted"""
    images = {}

    ### Load flickr_27 logos
    # Read training dataset file
    if source == constants.Dataset.Flickr27 or source == None:
        df: pd.DataFrame = pd.read_csv(constants.flickr_27_test_dataset_file, delimiter='\t', header=None)
        # Loop through data frame
        for i in df.index:
            image_file: str = df.loc[i][0]      # Image name
            label: str =  df.loc[i][1]          # Image label (what logo it is)
            image = load_image(constants.flickr_27_images_folder + image_file)      # Load the image into memory
            
            # Check if label exists in dictionary
            if images.get(label) != None:
                images[label].append(image)
            else:
                images[label] = [image]

    return images