# Import needed libraries
import numpy as np
import keras

# Load and process dataset, return array ready for training
## Define function
def load_data(num_classes=10, input_shape=(28,28,1)):

    ## Load MNIST dataset and split it between train and test set
    ## As arrrays: x -> (num_samples, 28, 28) and y -> integer 0-9
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    ## Scale images to the [0,1] range (pixel values, nn works better with small numbers)
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    ## Make sure images have shape (28, 28, 1) ->Add channel dimension ('color' grayscale)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    ## Convert class vectors to binary class matrices (e.g. 3 -> [0,0,1,0,0,0,0,0,0])
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    ## Array ready for training
    return x_train, y_train, x_test, y_test
