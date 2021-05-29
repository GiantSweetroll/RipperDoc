from neural_network import NeuralNetwork

import file_operations as io
import os
import constants
import file_operations
import datetime
import model_arch as m
import tensorflow.keras as keras

# Training params
batch_sizes: list = [1, 2, 4, 8, 16, 32, 64]
initial_learning_rates:list = [1.0, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.000001]
loss_functions = ["categorical_crossentropy", "sparse_categorical_crossentropy", "kullback_leibler_divergence"]
epochs = 50
trials = 5

# Helper functions
def generate_tensorboard_filename(
    model_name:str, 
    loss_function:str,
    optimizer_function:str,
    initial_learning_rate:int,
    batch_size:int,
    trial:int,
):
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + " - " + model_name + " loss-" + loss_function + " optimizer-" + optimizer_function + " lr-" + str(initial_learning_rate) + " batch_size-" + str(batch_size) + " t" + str(trial)

def generate_optimizers_list(lr):
    ls = []

    ls.append(keras.optimizers.Adadelta(learning_rate=lr))      # Adadelta
    ls.append(keras.optimizers.Adagrad(learning_rate=lr))       # Adagrad
    ls.append(keras.optimizers.Adam(learning_rate=lr))          # Adam
    ls.append(keras.optimizers.Adamax(learning_rate=lr))        # Adamax
    ls.append(keras.optimizers.Ftrl(learning_rate=lr))          # Ftrl
    ls.append(keras.optimizers.Nadam(learning_rate=lr))         # Nadam
    ls.append(keras.optimizers.RMSprop(learning_rate=lr))       # RMSprop
    ls.append(keras.optimizers.SGD(learning_rate=lr))           # SGD

    ls_name = []

    ls_name.append("Adadelta")
    ls_name.append("Adagrad")
    ls_name.append("Adam")
    ls_name.append("Adamax")
    ls_name.append("Ftrl")
    ls_name.append("Nadam")
    ls_name.append("RMSprop")
    ls_name.append("SGD")

    return ls, ls_name

def train(model_arch, model_name:str) :
    tensorboard_filename = ""
    csv_filename = ""

    print("Begin training " + model_name + "...")
    for i in range(trials):
        print("Trial:", i)
        model:sequent = model_arch
        for loss in loss_functions:
            for lr in initial_learning_rates:
                for batch_size in batch_sizes:
                    optimizers, optimizer_names = generate_optimizers_list(lr)
                    for optimizer, optimizer_name in zip(optimizers, optimizer_names):
                        tensorboard_filename = generate_tensorboard_filename(model_name, loss, optimizer_name, lr, batch_size, i)
                        csv_filename = model_name + "/" + generate_tensorboard_filename(model_name, loss, optimizer_name, lr, batch_size, i)
                        model.compile(optimizer, loss, metrics=["accuracy"])

                        # Train
                        ai = NeuralNetwork(model=model, tensorboard_file_name=tensorboard_filename, csv_file_name=csv_filename)
                        ai.train(batch_size=batch_size, epochs=epochs,)
                        ai.save(constants.model_loc + model_name + "/" + model_name + " loss-" + loss + " optimizer-" + optimizer_name + " lr-" + str(lr) + " batch_size-" + str(batch_size) + " t" + str(i))
    print(model_name + " completed!")

# MobileNetV2
train(m.MOBILENETV2, "MobileNetV2")
print("")

# Logo Recognition Arch from Paper
train(m.logo_recog(len(constants.labels)), "Logo Recog")
print("")

# Custom Model
train(m.custom_model((constants.image_width, constants.image_height, constants.color_channels), len(constants.labels)), "RipperDoc Custom")
print("")

# Xception
constants.image_width = 299
constants.image_height = 299
train(m.XCEPTION, "Xception")



# # Load AI
# print("Loading AI...")
# ai = NeuralNetwork(model=io.load_model(constants.model_loc + "logo_recog"))
# # ai = NeuralNetwork()
# print("AI loaded successfully")

# ai.train(batch_size=64, epochs=50)
# ai.save(constants.model_loc + ai.get_model().name)