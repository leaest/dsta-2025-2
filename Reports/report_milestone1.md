# Milestone 1 Report
## 1 - Dataset Overview
### What is the Dataset about?
The MNIST dataset is a combination of two datasets from the National Institute of Standards and Technology (NIST). Both parts are of equal size, one sourced from Census Bureau employees and the other from high school students. In total, the dataset contains 70,000 data points.
It includes only two columns: image and label. The image column contains a black-and-white picture of a single handwritten digit with a resolution of 28×28 pixels. The corresponding label indicates which of the ten classes the digit belongs to, representing the numbers 0 through 9. Each class contains 7’000 images, with 10% allocated to the test set. Overall, both the training and test sets follow the same distribution in terms of source and number of samples per digit.
This makes the dataset particularly useful for those who want to experiment with machine learning algorithms or pattern recognition techniques with minimal preparation and formatting effort.

### Applications
Since the digits are treated as categorical labels rather than numerical values, the dataset is used to train machine learning models for classification, not regression.
Therefore, it is not suitable for predicting continuous numerical values or performing quantitative calculations. The use of this dataset enables models to learn how to classify handwritten digits, which can, for example, be applied to analyze handwritten text more quickly and efficiently.

## ## 2 - Code Base
To save the Python file in our repository, we first need to navigate to the corresponding project directory. We get there using the command:
`cd ~/dsta-2025-2`

Due to the branch protection settings we put in place in our repository, it is not possible to push changes directly to the *main* branch. This is why we have to create a feature branch, where we can make changes that will later be reviewed by the other member and merged into the *main* branch via a pull request. To check whether we are currently on the *main* branch, we use:
`git status`

Since this is our first commit, we should still be on the main branch. Next, we create a new branch (called `add-python-file`) where we add the code:
`git checkout -b add-python-file`. With the code `git checkout <branch-name>` we are able to switch between our branches and with `git branch` we are able to see all our local branches. The one activated is marked with a *.
 
It is now possible to download the code file directly form GitHub via:
`wget https://raw.githubusercontent.com/keras-team/keras-io/master/examples/vision/mnist_convnet.py`

This downloads the `mnist_convnet.py` file directly into `dsta-2025-2`.

After downloading we check if the file contains the correct code. In our first attempt, we skipped this step and accidentally pushed a file containing the HTML source code of the GitHub page instead of the Python script. We decided to close the pull request and restart the process correctly.

## 3 - Commit Workflow
###  Preparation
Before pushing anything to GitHub, we need to ensure that our working environment is properly connected to your account so that the contributions are correctly registered.

Check with method our Git repository currently uses:
`git remote -v`

| HTTPS | SSH |
|-------|-----|
| `origin https://github.com/...`<br>`origin https://github.com/...` | `origin git@github.com:...`<br>`origin git@github.com:...` |

In our case the Git repository used HTTPS, but we decided to switch to SSH to avoid entering our username and access token every time we push or pull something.


**We performed the switch using the following steps:**
1. Generate the SSH key: `ssh-keygen -C "e-mail address"`<br>- For "Enter file in which to save the key..." press `Enter` for default location<br>- For "Enter passphrase (empty for no passphrase):" press `Enter`, we don't need additional security

2. Start the SSH agent and add the key to it:<br>`eval "$(ssh-agent -s)"`<br>`ssh-add ~/.ssh/id_rsa`

3. Copy the output of: `cat ~/.ssh/id_rsa.pub`<br>This is the public key.

4. Add the public key to GitHub under Settings/SSH and GPG keys/New SSH key

5. We check if the connection works: `ssh -T git@github.com`<br>The following message appears:<br>`The authenticity of host 'github.com (140.82.121.4)' can't be established.`<br>`RSA key fingerprint is SHA256:  [Combination of letters and numbers]`<br>`This key is not known by any other names`<br>`Are you sure you want to continue connecting (yes/no/ [fingerprint])?`<br><br>Because we want trust the host (GitHub), type `yes`

6. Change repository remote HTTPS to SSH: `git remote set-url origin git@github.com:leaest/dsta-2025-2.git`

7. Verify the change: `git remote -v`<br>`origin git@github.com:leaest/dsta-2025-2.git (fetch)`<br>`origin git@github.com:leaest/dsta-2025-2.git (push)`

The setup is complete and ready to use.

### Commit Python File
To upload the file from the local repository to GitHub, we use the following commands (which also apply to future commits):
`git add mnist_convnet.py`
`git commit -m \'Summary of what was done\' -m \'Detailed information on what was done`
`git push origin add-python-file`

If the operation was successful, the changes appear on GitHub under the newly crated branch. From there, we opened a pull request to propose merging the changes into the *main* branch and review them before approval.
After having approved the changes, the feature branch must be merged into the *main* branch, otherwise the main-branch stays unaffected. Afterwards the feature branch could be deleted.


## 4 - Run the Code
### Explain in detail which steps were necessary to run the code. How did you install Python?
Since we are working with Linux it was not nessessary to install Python as it comes pre-installed. Nevertheless, we check the exact Python version using `python3 --version`. In our case, it is version 3.10.

Before running the code it was nessessary to create a virtual environment. This ensures that the projects runs in an isolated enivromnet where the nessessary dependencies can be managed seperatly. This is helpful to avoid conflicts with packages used in other projects because different projects could potentially use different versions of the same package. Furthermore the virtual environment helps to keep an overview which packages are used for which projects.

This is done by creating a .venv folder on the local repository with `python3 -m venv .venv`.
After having activated the virtual environment with (`source .venv/bin/activate`) the next mandatory step was to install the required packages/dependencies. Since the virtual environment folder should be versioned, we excluded the folder by creating a gitignore and adding the .venv folder to it with `echo ".venv/" > .gitignore`.

Before being able to install the correct packages, we had to ensure that we have pip installed with `pip version`. Since pip was not installed, we had to do so my running: `sudo apt install python3-pip -y`. After installing the required packages  `pip install <packagename>` I had to rename the python file with `mv keras.py mnist_convnet.py` because there were some conficts since the python file cannot have the same name as one of the packages.
Eventually were able to run the python code with `python mnist_convnet.py`

### Find out what versions are being used to run the code
To find out what dependencies are used we run the command `pip freeze > requirements.txt`
These include
- numpy = 3.12.0
- keras = 3.12.0
- keras requires TensorFlow = 2.20.0

These three dependencies depend on other packages. The full list can be seen under "requirements.txt".

### Are the versions dependent on the system the code is being run on?
To run the code on other systems, the correct versions of the dependencies must be installed. This can be done with `pip install -r requirements.txt`. Furthermore, it is recommended that on each machine a virtual environment is set up, to avoid the conflicts explained above.
If the python-file works with file paths, it is important that the paths are defined with `pathlib` since Windows and Mac / Linux use different path seperators. This is however not that important this time, because no paths are used in the python file.


## 5 - Understand the Code
### Input and Output
The data comes from the MNIST dataset, available at https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz , and is stored locally in the `.keras` folder. The inputs to the neural network are the images from the MNIST dataset, as described in *1 - Dataset Overview*. The data is reshaped to `(28, 28, 1)` so that the `Conv2D` layer can interpret it correctly. This shape indicates that each image is 28×28 pixels with a single color channel (grayscale). The output, on the other hand, is a vector of ten probabilities representing the predicted digit class (0-9).

### Keras and TensorFlow
TensorFlow provides the core functionality for building and running machine learning models. This includes mathematical operations, optimization, and efficient computation.
Keras offers a simple and intuitive way to build and train models on top of TensorFlow. It simplifies model development by providing a clear, user-friendly framework for defining layers, compiling models, and performing training and evaluation.

### Data Loading
The dataset is loaded using Kera's built-in function:
`(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()`

In this step, the data is automatically divided into training and test sets for both images (`x`) and labels (`y`).

### Dependencies
The code uses the following dependencies:
- numpy: Used for numerical operations and array manipulation, such as reshaping the data.
- keras: Neural network library for building, training, and evaluating models.
- keras.layers: Contains the building blocks of the network, including convolutional, pooling, flattening, dropout, and dense layers.

### Neural Network Architecture
Keras built a convolutional neural network (CNN). It consists of:
- Two `Conv2D` + `MaxPooling2D` blocks for feature extraction
- `Flatten` layer to convert 2D features to 1D
- `Dropout` layer for regularization
- `Dense softmax` layer with 10 outputs for classification

The first two try to find pattens in the images. The `Dropout` layer prevents over-fitting by turning off some neurons during the training and therefor forcing the network to use different neurons.
The `Dense softmax` converts the output values into probabilities. Basically, the model "votes" on how confident it is, for each of the 10 different digits. The one with the highest percentages will be the answer of the model.

The model begins training for 15 epochs with a batch size of 128 using the `Adam` optimizer and `categorical crossentropy` loss. With each round the model improves based on what it learned in the previous round.
Running the code reveals that the model came up with about 35'000 parameters.

The expected final test accuracy is ~ 99%, which matches the observed results:
- Test loss: 0.02
- Test accuracy: 0.99

### Why a Neural Network is needed
Handwritten digits vary in style, thickness, and orientation. Simple rule-based methods or linear models cannot capture these complex patterns. A CNN can automatically learn spatial features (e.g. edges and shapes), enabling accurate classification. The high test accuracy demonstrates the network's ability to generalize to new, unseen digits.

## 6 - Project Documentation
The `README` file was created directly on GitHub at the time the repository was initially set up.

### 8 - Report Submission
A new folder named *Reports* was created by using `mkdir Reports`. Inside this folder we used `touch report_milestone1.md` to generate the markdown file.
To edit the markdown file, we can either use `vim report_milestone1.md` or if we want to use a different editor such as VS-Code we can use `code report_milestone1.md`. For this last command to work, it must correctly be set up in VS Code by entering the command `shell` and selecting `Shell Command: Install 'code' command in PATH`.



