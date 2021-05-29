import constants
import methods
import model_arch as models
import numpy as np
import file_operations
import tensorflow as tf
import datetime

class NeuralNetwork():
    
    #Constructor
    def __init__(self, 
        model = None,
        tensorboard_file_name:str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
        csv_file_name:str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
    ):
        """A class to represent the neural network object"""
        if model == None:
            # Use Xception model
            print("Building new Neural Network model...")
            # model = models.MOBILENETV2
            # model = models.custom_model((constants.image_width, constants.image_height, constants.color_channels), len(constants.labels))
            model = models.logo_recog(len(constants.labels))

            # Learning rate scheduler
            lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
                initial_learning_rate=0.001,
                decay_steps=100000,
                decay_rate=0.96,
                staircase=True
            )

            model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule), metrics=['accuracy'])  # Compile the model
            print("Model compiled!")
        elif not model._is_compiled:
            print("Model was not compiled, compiling...")
            model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule), metrics=['accuracy'])  # Compile the model
            print("Model compiled!")

        self.__model = model
        self.__tensorboard_file_name = tensorboard_file_name
        self.__csv_file_name = csv_file_name
    
    #Setters and Getters
    def get_model(self):
        return self.__model
    
    def get_model_summary(self):
        return self.get_model().summary()
            
    def set_model(self, model):
        self.__model = model
        
    #Other Methods
    def train(self,
                batch_size:int = constants.default_batch_size, 
                epochs:int = 10, 
                verbose:int = 2):
        """
        Train the neural network model
        batch_size: amount of images to train with at one given time
        epochs: training iterations to do
        verbose: verbose mode. (0=silent, 1=minimal, 2=every batch)
        validation_data: the data used to validate the neural network model
        """
        width = constants.image_width
        height = constants.image_height
        color_channels = constants.color_channels

        # Load training and test images
        print('Loading training and validation images....')
        train_ds, val_ds = file_operations.load_training_dataset(augment=True, batch_size=batch_size)
        x_train, y_train = next(iter(train_ds))
        x_val, y_val = next(iter(val_ds))
        # Convert labels into 1 hot format
        y_train = tf.keras.utils.to_categorical(y_train, len(constants.labels))
        y_val = tf.keras.utils.to_categorical(y_val, len(constants.labels))
        print('Training and validation images loaded.')
        
        # Prepare tensorboard
        log_dir = "L:/For Machine Learning/Project/RipperDoc/models/logs/fit/" + self.__tensorboard_file_name
        tensorboard_callback = tf.keras.callbacks.TensorBoard(
            log_dir=log_dir, 
            histogram_freq=1,
            embeddings_freq=1,
            write_images=True,
        )
        
        # Configure callbacks
        early_stopping_callback = tf.keras.callbacks.EarlyStopping(
            # Stop training when `val_loss` is no longer improving
            monitor="val_loss",
            # "no longer improving" being defined as "no better than 1e-2 less"
            min_delta=1e-2,
            # "no longer improving" being further defined as "for at least 10 epochs"
            patience=10,
            verbose=1
        )
        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            # Path where to save the model
            # The two parameters below mean that we will overwrite
            # the current checkpoint if and only if
            # the `val_loss` score has improved.
            # The saved model name will include the current epoch.
            filepath= constants.model_loc + "ripperdoc_{epoch}",
            save_best_only=True,  # Only save a model if `val_loss` has improved.
            monitor="val_loss",
            verbose=1,
            save_weights_only=False
        )
        csv_logger = tf.keras.callbacks.CSVLogger(
            'L:/For Machine Learning/Project/RipperDoc/models/' + self.__csv_file_name + '.csv',
            append=False
        )

        # Train the neural network
        print('Begin training AI....')
        return self.get_model().fit(x_train,
            y_train,
            batch_size = batch_size, 
            epochs = epochs, 
            verbose = verbose, 
            validation_data = (x_val, y_val),
            callbacks=[
                tensorboard_callback, 
                early_stopping_callback, 
                # model_checkpoint_callback, 
                csv_logger
            ]
        )
        print('Training AI completed!')

    def save(self, path):
        """save the current state of the model as a file so that it can be loaded in the future"""
        print('Saving AI model...')
        self.get_model().save(path)
        print('AI model saved!')
        
    def evaluate(self, data, labels, verbose = 2):
        """Function to evaluate the accuracy of the model"""
        self.get_model().evaluate(data, labels, verbose = verbose)
    
    def predict(self, image) -> str:
        """
        Method to predict what character is the image, returns the logo name.
        image: image tensor
        """
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])
        input_arr = tf.image.resize(input_arr, [constants.image_width, constants.image_height])
        input_arr = np.array(input_arr)
        input_arr /= 255        # Apply normalization

        # Make prediction
        prediction = self.get_model().predict(input_arr)
        pred_label:str = constants.labels[int(prediction.argmax().__str__())]

        return pred_label