from neural_network import NeuralNetwork

import file_operations as io
import tensorflow as tf
import os
import constants
import file_operations

# Load AI
print('Loading AI...')
ai = NeuralNetwork(model=io.load_model(constants.model_loc + 'logo_recog_65'))
print('AI loaded successfully')

ai.train(batch_size=64, epochs=50)
ai.save(constants.model_loc + ai.get_model().name)