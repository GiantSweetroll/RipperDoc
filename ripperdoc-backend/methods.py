from cv2 import cv2
import matplotlib.pyplot as plt
import numpy
import tensorflow as tf
import constants

def __convert_data_map_to_lists(data_map:{}):
    """Converts the data dictionary to a numpy array of the labels (keys as integers) and a numpy array of the images (used to insert into neural net model)"""
    raw_images:[] = []
    image_labels:[] = []
    for label in data_map:
        for image in data_map[label]:
            raw_images.append(image)
            image_labels.append(label)
    
    return raw_images, numpy.array(image_labels)

def __resize_image(image, width:int = constants.image_width, height:int = constants.image_height):
    """Method to resize image, aspect ratio not preserved"""
    image_resized = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)
    return image_resized

def __resize_images(images, width:int = constants.image_width, height:int = constants.image_height):
    """Method to convert a list of images"""
    for i in range(len(images)):
        image = __resize_image(images[i], width, height)
        images[i] = image
    return images

def __convert_to_numpy_arr(images, width, height, color_channels):
    """Method for converting the list of images as a numpy array fit for neural network input"""
    arr = numpy.array(images)
    array = numpy.zeros((len(images), width, height, color_channels)) if color_channels != 1 else numpy.zeros((len(images), width, height))
    if color_channels != 1:
        for i in range(len(images)):
            array[i,:,:,:] = images[i]
    else:
        for i in range(len(images)):
            array[i,:,:] = images[i]
    
    return array

def __shape_image_for_2d_mlp_input(images, width:int = constants.image_width, height:int = constants.image_height, color_channels:int = constants.color_channels):
    """A method to reshape the images to be ready for neural net input"""
    #Color channels is the amount of possible colors -> grayscale = 1, colored = 3
    
    #Sometimes Keras puts color channels first before width and height, so we need to check for that
    if tf.keras.backend.image_data_format() == 'channels_first':
        reshaped_images = images.reshape(images.shape[0], color_channels, width, height)
    else:
        reshaped_images = images.reshape(images.shape[0], width, height, color_channels)
    
    reshaped_images = reshaped_images.astype('float32')
    reshaped_images /= 255      #Divide by 255 because 255 color scheme, so that the input will be decimals between 0-1
    
    return reshaped_images

def __convert_labels_to_one_hot(labels, categories:int):
    """Convert the labels to one-hot format (so that we know what character it is)"""
    new_labels:[] = __convert_labels_to_index_correspondence(labels)
    return tf.keras.utils.to_categorical(new_labels, categories)

def __convert_labels_to_index_correspondence(labels):
    """Method to convert the characters of the sorted labels to correspond to the index of the labels in constants"""
    new_labels:[] = []
    i = -1
    current_brand = ""
    prev_brand = ""
    for a in range(len(labels)):
        current_brand = labels[a]
        if current_brand != prev_brand:
            i+=1
        prev_brand = labels[a]
        new_labels.append(str(i))
    return new_labels

def prepare_images_for_mlp_input(images, 
                                    width:int = constants.image_width,
                                    height:int = constants.image_height,
                                    color_channels = constnats.color_channels):
    # Prepare the images and format them to be compatible with the given neural network model
    images = __resize_images(images, width, height)   #Resize the images to a uniform size
    images = __convert_to_numpy_arr(images, width, height, color_channels)    #Convert the list to a numpy array
    images = __shape_image_for_2d_mlp_input(images, width, height, color_channels)    #Convert image_array according to keras specification (color channels first or last), and normalize the images to be between 0 and 1
    return images

def get_image_and_label_for_mlp_input(image_map:{}, width:int = constants.image_width, height:int = constants.image_height, color_channels = constants.color_channels):
    """Method to automatically format input image dictionary to be usable for neural network input. Method returns the formatted image as 4D numpy list and the associated labels"""

    image_list, image_labels = __convert_data_map_to_lists(image_map)    #Convert the dictionary to a list, and convert the keys to a list as well that matches the size of the image list

    image_list = prepare_images_for_mlp_input(image_list)   # Prepare the images and format them to be compatible with the given neural network model

    image_labels = __convert_labels_to_one_hot(image_labels, len(constants.labels))    #Convert the labels to one-hot format for neural network classification
    
    return image_list, image_labels

def show_prediction_graph(image, prediction:str):
    """Method to display the prediction and the image in the same matplotlib graph"""
    plt.title("Prediction: " + prediction)
    plt.imshow(image, cmap="gray")
    plt.show()

def show_prediction_graph_with_label(image, prediction:str, label:str):
    """Method to display the prediction and the image in the same matplotlib graph. The actual label is also displayed"""
    plt.title("Prediction: " + prediction + " Label: " + label)
    plt.imshow(image, cmap="gray")
    plt.show()

def read_image_from_bytes(bytes_str:str):
    """ Read image from bytes string"""
    nparr = numpy.frombuffer(bytes_str, dtype = numpy.uint8)
    img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
    return img