#Milestone 1
##Exercise 1
###What is the dataset about?
The MNIST dataset is a combination of two datasets from the National Institute of Standards and Technology (NIST). Both parts are of equal size, one sourced from Census Bureau employees and the other from high school students. In total, the dataset contains 70,000 data points.
It includes only two columns: image and label. The image column contains a black-and-white picture of a single handwritten digit with a resolution of 28×28 pixels. The corresponding label indicates which of the ten classes the digit belongs to, representing the numbers 0 through 9. Each class contains 7’000 images, with 10% allocated to the test set. Overall, both the training and test sets follow the same distribution in terms of source and number of samples per digit.
This makes the dataset particularly useful for those who want to experiment with machine learning algorithms or pattern recognition techniques with minimal preparation and formatting effort.

###What problem is solved by the machine learning models trained on it?
Since the digits are treated as categorical labels rather than numerical values, the dataset is used to train machine learning models for classification, not regression.
Therefore, it is not suitable for predicting continuous numerical values or performing quantitative calculations. The use of this dataset enables models to learn how to classify handwritten digits, which can, for example, be applied to analyze handwritten text more quickly and efficiently.


##Exercise 4
Explain in detail which steps were necessary to run the code. How did you install 
Python?
Since we are working with Linux it was not nessessary to install Python as it comes pre-installed. 
Before running the code it was nessessary to create a virtual environment. This ensures that the projects runs in an isolated enivromnet where the nessessary dependencies can be managed seperatly. This is helpful to avoid conflicts with packages used in other projects because different projects could potentially use different versions of the same package. Furthermore the virtual environment helps to keep an overview which packages are used for which projects.
This is done by creating a .venv folder on the local repository with `python3 -m venv .venv`.
After having activated the virtual environment with (`source .venv/bin/activate`) the next mandatory step was to install the required packages/dependencies.
These include
    - numpy = 3.12.0
    - keras = 3.12.0
    - keras requires TensorFlow = 2.20.0

These three dependencies depend on other packages. The full list can be seen under "requirements.txt".

##Exercise 5
Data comes from: https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz and is stored locally in a the .keras folder.

- Keras built a convolutional neural network with 2 Conv2D + MaxPooling blocks, then Flatten, Dropout, and a Dense softmax layer with 10 outputs.
- After this, the model begins training for 15 epochs using the Adam optimizer and categorical crossentropy loss.
- Expected final test accuracy is ~99% on MNIST.
Test Results after Running Code:
- Test loss: 0.026664797216653824
- Test accuracy: 0.9908999800682068
