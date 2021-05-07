from PIL import Image
import base64
import cv2
import glob
import io
import numpy as np
import pandas as pd
import constants
import tensorflow as tf

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

def load_model(path:str):
    """
    Method to laod the desired neural network model
    path: the path of the model file, complete with .h5 extension
    """
    return tf.keras.models.load_model(path)

def read_image_from_bytes(base64_string:str):
    """ Read image from bytes (base64) string"""
    decoded_data = base64.b64decode(base64_string)
    np_data = np.frombuffer(decoded_data, np.uint8)
    return cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

def convert_img_to_base64(image):
    """Convert cv2 image into base64 bytes string"""
    retval, buffer = cv2.imencode('.jpg', image)
    base64_string = base64.b64encode(buffer)
    return base64_string