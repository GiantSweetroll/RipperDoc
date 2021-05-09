import tensorflow as tf

def normalize_dataset(ds, normalization_layer = None):
    """ Normalize the dataset """
    if normalization_layer == None:
        normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
    return ds.map(lambda x, y: (normalization_layer(x), y))