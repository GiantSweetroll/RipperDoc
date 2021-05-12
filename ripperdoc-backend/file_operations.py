from PIL import Image

import constants
import tensorflow as tf
import methods
import io
import base64
from io import BytesIO

def load_training_dataset(
    batch_size:int = constants.default_batch_size,
    img_width:int = constants.image_width, 
    img_height:int = constants.image_height,
    validation_split:float = 0.2,
    augment:bool = False,
):
    """ Load training and validation images using tensorflow"""
    # Get dataset directory
    data_dir:str = constants.dataset_loc     # Dataset directory
    
    # Get training dataset
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=validation_split,
        subset='training',
        seed=123,
        image_size=(img_width, img_height),
        batch_size=batch_size
    )
    
    # Get validation dataset
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=validation_split,
        subset='validation',
        seed=123,
        image_size=(img_width, img_height),
        batch_size=batch_size
    )

    # Normalize data
    normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
    train_ds = methods.normalize_dataset(train_ds, normalization_layer)
    val_ds = methods.normalize_dataset(val_ds, normalization_layer)

    # Configure autotune
    AUTOTUNE = tf.data.AUTOTUNE

    if augment:
        # Shuffle training dataset
        train_ds = train_ds.shuffle(1000)

        # Apply data augmentation on training dataset
        data_augmentation = tf.keras.Sequential([
            tf.keras.layers.experimental.preprocessing.RandomFlip("horizontal_and_vertical"),
            tf.keras.layers.experimental.preprocessing.RandomRotation(0.2, fill_mode='constant'),
            # tf.keras.layers.experimental.preprocessing.RandomContrast(0.2)
        ])
        train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=AUTOTUNE)

    # Configure performance
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds

def load_model(path:str):
    """
    Method to laod the desired neural network model
    path: the path of the model file, complete with .tf extension
    """
    try:
        return tf.keras.models.load_model(path)
    except IOError as e:
        print(e)
        return None

def load_image(path:str):
    return Image.open(path)

def convert_png_to_jpg(image:Image):
    return image.convert('RGB')

def get_as_base64_from(image: Image):
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")

    return base64.b64encode(img_bytes.getvalue())

def convert_base64_to_image(base64str:str):
    base64_bytes = base64.b64encode(base64str.encode('utf-8'))
    im_file = BytesIO(base64_bytes)

    return Image.open(im_file)