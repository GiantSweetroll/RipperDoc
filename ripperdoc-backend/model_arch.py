import tensorflow as tf
import tensorflow.keras.layers as layers
import constants

class LogoRecog(tf.keras.models.Sequential):
    def __init__(self, class_count:int):
        super().__init__(layers=[
            layers.Conv2D(32, kernel_size=(5, 5), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPooling2D(strides=2),
            layers.Conv2D(32, kernel_size=(5, 5), activation='relu'),
            layers.AveragePooling2D(strides=2),
            layers.Conv2D(64, kernel_size=(5, 5), activation='relu'),
            layers.AveragePooling2D(strides=2),
            layers.Dense(64),
            layers.Dense(33, activation='softmax')
        ])

MOBILENETV2 = tf.keras.applications.MobileNet(
    classes=len(constants.labels),
    classifier_activation='softmax',
    weights=None,
    dropout=0.01
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