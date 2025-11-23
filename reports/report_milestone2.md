# Milestone 2 Report
## 1 - Git Repository and .gitignore Management

## 2 - Theoretical Questions

## 3 - Neural Network Functionality Implementation
With the completion of Milestone 1, the original `mnist_convnet.py` script was fully functional. It successfully loaded and prepared the MNIST dataset, then built and trained neural network.
Although we can verify whether the model works at the end of the process when it prints the comparison table of predictions and true values, we added confirmation messages so that the completion of each process can be observed.

### Saving the Trained Model
The code has now been extended to include saving, loading, and prediction.  
Model saving is implemented by defining a full file path, which is useful in case we want to change it later. Currently, the model is saved in a separate directory called `models`.

Because our project specifies TensorFlow **2.20.0** in `requirements.txt`, the model is saved in the recommended `.keras` format rather than the older `.h5` format. The resulting file is named `CNN_model_mnist.keras`.

### Loading the Trained Model
Loading the model works similarly to saving it. Since the full path (including the filename) is already defined during the saving process, we can reuse it when loading. This ensures consistency and minimizes the chance of errors when changing file names or directories.

### Prediction
For prediction, a small subset of the test data is used to verify that the model works correctly. Evaluating all 10'000 test images is unnecessary, so we selected the first 10 observations as a sample.

Predicted labels and true class labels are then combined in a table for horizontal comparison. Given that the test accuracy is more than 99%, we expect all sampled predictions to be correct. To observe errors we would need a bigger sample. Our goal is to verify functionality rather than optimize accuracy so we consider this unnecessary.

Predicted classes (`pred_class`) are determined by selecting the class with the highest predicted probability. True classes (`true_class`) are identified from the binary label array (e.g., `[0, 0, 1, 0, 0, 0, 0, 0, 0, 0]` -> class 2). The comparison table allows for easier visual verification, particularly if the sample size increases.

## 4 - Code Modularization & Project Structure
Before running `main.py`, a `__init__.py` file is created in the `src` directory. This marks the folder as a Python package and enables the import of submodules. Without this file, `main.py` cannot access the functions defined in the modules.

By structuring the code so that `main.py` calls functions from separate modules, the project becomes more organized, maintainable, and scalable. This improves the project structure and prevents large, unmaintainable files.

### Reasoning Behind the Modularization
To separate the project’s functionalities clearly, the code was divided into several modules. Module and function names were chosen deliberately to avoid confusion between file names and function names.

|Role|Module|Function(s)|
|---|---|---|
|Loading Data|`data_prep.py`|`load_data`|
|Building Model|`neuralnet_architecture.py`|`build_neuralnet`|
|Training|`neuralnet_training.py`|`train_neuralnet`  <br>`save_model`|
|Loading Model|`neuralnet_loading.py`|`load_trained_model`|
|Predicting|`neuralnet_prediction.py`|`predict_sample`|

Each module defines functions and returns results. `main.py` handles calling these functions and printing outputs or confirmation messages.

Because each module is essentially a separate Python script executed independently, all necessary packages must be imported within each module. This was initially forgotten, which caused the code not to run and took a significant amount of time to debug—especially since we had done the same thing correctly in the original `mnist_convnet.py` script. Once this is understood, it is unlikely to be forgotten in the future.

**Loading Data**
This module follows the same process as in `mnist_convnet.py`. The function defines the parameters used, loads the data, splits it into training and test sets, scales and reshapes the images, and converts the class vectors into one-hot encoded matrices. The function returns the prepared training and test data arrays.

`main.py` calls this function, and confirmation is provided by printing the shapes of the resulting arrays:
x_train: (60000, 28, 28, 1)
y_train: (60000, 10)
x_test: (10000, 28, 28, 1)
y_test: (10000, 10)

This implies that we have 60'000 observaitons for training and 10'000 for test. We can also see the dimensions of the image (which we have specifies) of 28x28 pixels and 1 for grayscale. The label variable on the other hand has 10 values (numbers 0-9). This tells us that our function has prepared the data correctly.

Data loading and preprocessing are combined in a single function because the raw data is not used for other purposes. If future use cases arise, preprocessing steps would probably be similar, otherwise, raw data handling would differ entirely. Therefore, it makes sense for our project to combine these steps 

**Building Model**
This module defines the neural network architecture. Input shape and number of classes are parameters, making it adaptable to other datasets if needed. The rest of the implementation mirrors `mnist_convnet.py`.
`main.py` calls this function and verifies the model by printing its summary.

We separate the model construction from other processes because their tasks are not related. Building the model architecture is not similar to any other process that follows.

**Training**
The training function receives the model and data, along with batch size and number of epochs (adaptable if needed), and returns the trained model. The trained model is then saved using a second function, with the storage location and filename defined for organization. 
`main.py` executes both functions and prints confirmation messages. It is optional to change the filename if needed. At the beginning, saving did not work because the path needed to explicitly go out of the current folder into the target folder (e.g., `../models/CNN_model.keras`). Additionally, setting `path=""` caused issues because it overwrote the default path in the function with an empty string, so the function did not know where to save the model. For simplicity, we decided to leave the path change as a commented option if the user wants to modify it.
The evaluation is also performed in `main.py` rather than a module, as it is primarily for output rather than reusable functionality.


Training and saving are in the same module because they are closely related: training generates a model that should immediately be saved. Separating them would rarely provide additional benefit.

**Loading Model**
This module handles loading the trained model. The full path is also predefined.
`main.py` calls the function and prints a confirmation message.

Loading is separated from prediction so the model can be reused for multiple predictions without repeated reloads.

**Predicting**
The prediction module calculates the probability of each image belonging to each class and selects the class with the highest probability. The function returns the predicted class and the true class. It is essentially the same as described in *3 - Neural Network Functionality Implementation*.

In `main.py`, a sample of 10 observations is selected. These are displayed in a horizontal comparison table for clarity.

## 5 - Dependency Management

## 6 - Dockerization