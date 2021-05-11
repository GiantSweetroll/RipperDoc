import os


image_width = 224
image_height = 224
color_channels = 3
default_batch_size = 16

dataset_loc:str = "L:/For Machine Learning/Project/RipperDoc/dataset/"
model_loc:str = "L:/For Machine Learning/Project/RipperDoc/models/"

labels:[] = os.listdir(dataset_loc)        # The classifications