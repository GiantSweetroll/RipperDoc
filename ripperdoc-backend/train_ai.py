from neural_network import NeuralNetwork

import file_operations as io
import tensorflow as tf
import os

# Load AI
print('Loading AI...')
ai = NeuralNetwork(model=io.load_model('ai/xception_hn'))
print('AI loaded successfully')

ai.train(batch_size=16, epochs=50)

# # Preparing for Tensorflow Serving
# model_directory = 'ai/'
# print("Model directory:", model_directory)

# version = 1

# export_path = os.path.join(model_directory, str(version))
# print('export_path = {}\n'.format(export_path))

# tf.keras.models.save_model(
#     ai.get_model(),
#     export_path,
#     overwrite=True,
#     include_optimizer=True,
#     save_format=None,
#     signatures=None,
#     options=None
# )