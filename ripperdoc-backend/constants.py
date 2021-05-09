import enum

image_width = 299
image_height = 299
color_channels = 3
default_batch_size = 16

labels:[] = ["Apple", "HP", "Google", "Intel"]

# Flickr 27 dataset
flickr_27_dataset_folder = 'datasets/flickr_logos_27_dataset/'
flickr_27_images_folder = flickr_27_dataset_folder + 'ripperdoc_filtered/'
# flickr_27_images_folder = flickr_27_dataset_folder + 'flickr_logos_27_dataset_images/'
flickr_27_training_dataset_file = flickr_27_dataset_folder + 'trimmed_training_dataset.txt'
flickr_27_validation_dataset_file = flickr_27_dataset_folder + 'trimmed_validation_dataset.txt'

class Dataset(enum.Enum):
    Flickr27 = 1
    Flickr32_plus = 2
    Selenium = 3
    Collector = 4