import os

image_width = 299
image_height = 299
color_channels = 3
default_batch_size = 16

dataset_loc:str = "L:/For Machine Learning/Project/RipperDoc/dataset"
labels:[] = os.listdir(dataset_loc)        # The classifications