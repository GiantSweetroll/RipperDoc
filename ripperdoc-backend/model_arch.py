import tensorflow as tf
import tensorflow.keras.layers as layers
import constants

MOBILENETV2 = tf.keras.applications.MobileNet(
    classes=len(constants.labels),
    classifier_activation='softmax',
    weights=None,
)

XCEPTION = tf.keras.applications.Xception(
    include_top=True, 
    weights=None, 
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=len(constants.labels),
    classifier_activation='softmax'
)

def custom_model(input_shape:(), class_count:int):
    model = tf.keras.models.Sequential(name='ripperdoc_custom')
    model.add(layers.Conv2D(16, kernel_size=(5, 5), activation='relu', input_shape=input_shape))
    model.add(layers.Conv2D(32, kernel_size=(5, 5),activation='relu'))
    model.add(layers.Conv2D(64, (5, 5), activation='relu'))
    # Reduce by taking the max of each 2x2 block
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    # Dropout to avoid overfitting
    model.add(layers.Dropout(0.25))
    # Flatten the results to one dimension for passing into our final layer
    model.add(layers.Flatten())
    # A hidden layer to learn with
    model.add(layers.Dense(64, activation='relu'))
    # Another dropout
    model.add(layers.Dropout(0.5))
    # Final categorization with softmax
    model.add(layers.Dense(class_count, activation='softmax'))

    return model

def logo_recog(class_count: int):
    return tf.keras.models.Sequential([
        layers.Conv2D(32, kernel_size=(5, 5), activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D(strides=2),
        layers.Conv2D(32, kernel_size=(5, 5), activation='relu'),
        layers.AveragePooling2D(strides=2),
        layers.Conv2D(64, kernel_size=(5, 5), activation='relu'),
        layers.AveragePooling2D(strides=2),
        layers.Flatten(),
        layers.Dense(64),
        layers.Dense(class_count, activation='softmax')
    ], name='logo_recog')