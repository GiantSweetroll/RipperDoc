import constants
import methods
import file_operations

class NeuralNetwork():
    
    #Constructor
    def __init__(self, model = None):
        """A class to represent the neural network object"""
        if model == None:
            model = methods.create_model(methods.get_input_shape(constants.color_channels, 
                                                                            constants.image_width, 
                                                                            constants.image_height), 
                                                                            len(constants.char_list))
        self.__model = model
    
    #Setters and Getters
    def get_model(self):
        return self.__model
    
    def get_model_summary(self):
        return self.get_model().summary()
            
    def set_model(self, model):
        self.__model = model
        
    #Other Methods
    def train(self,
              batch_size:int = 100, 
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

        #Load training and test images
        train_images, train_labels = methods.get_image_and_label_for_mlp_input(file_operations.load_training_images(), width, height, color_channels)
        test_images, test_labels = methods.get_image_and_label_for_mlp_input(file_operations.load_test_images(), width, height, color_channels)
        
        # Train the neural network
        return self.get_model().fit(train_images, 
                                    train_labels, 
                                    batch_size = batch_size, 
                                    epochs = epochs, 
                                    verbose = verbose, 
                                    validation_data = (test_images, test_labels))
        
    def save(self, filename):
        """save the current state of the model as a file so that it can be loaded in the future"""
        self.get_model().save("ai/" + filename + ".h5")
        
    def evaluate(self, data, labels, verbose = 2):
        """Function to evaluate the accuracy of the model"""
        self.get_model().evaluate(data, labels, verbose = verbose)
        
    def predict(self, image, show_pred_graph:bool = False) -> str:
        """Method to predict what character is the image, returns the image."""
        #If show_pred_graph = True, it will draw the image and the prediction in a matplotlib graph
        prediction = self.get_model().predict(image)
        prediction_argmax = prediction.argmax()
        predLabel:str = constants.labels[int(prediction_argmax.__str__())]
        
        if show_pred_graph:
            methods.show_prediction_graph(image.reshape(constants.image_width, constants.image_height, constants.color_channels), predLabel)
            
        return predLabel