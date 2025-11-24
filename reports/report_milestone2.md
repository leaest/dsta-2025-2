
# Milestone 2 Report
## 1 - Git Repository and .gitignore Management
The `.gitignore` file was already created in Milestone 1. However, in this earlier stage we had that `.gitignore` file on our main branch, so everytime someone would add something to the `.gitignore`, it the entire feature branch that person would be working on, would have to be merged into the main branch to make the `.gitignore` available for everyone else. This is problematic since merging a feature branch with the main branch clutters the git history. Secondly, a feature branch should only be merged into the main, if the entire feature that is to be implemented is working, since it could otherwise break all the code that has been working.
To avoid this issue, the changes on the `.gitignore` file can be tracked on its own branch. Whenever someone needs to add some files to the `.gitignore`, they would do that on said branch instead of the feature branch that they are working on. Important is, that when these changes are made, they need to be pushed immediately. In order to do that, the person needs to be on the gitignore branch and execute the following command `git add .gitignore`. This way only the changes on the  `.gitignore` file will be added for the commit (this is not per se mandatory if everything is done correctly but ensures that really only the changes to the git file will be committed to the gitignore branch). After staging the changes on the `.gitignore` the person commits them as usual and then pushes the update to the dedicated branch using `git push origin gitignore`. This ensures that the changes in the `.gitignore` are made available for all the people working on the project.
However, instead of merging the changes into the main, to make them available to everyone, all people working on their feature branches can run the command `git rebase gitignore`. This command updates the branch on which the code was run, so it basically takes all the commits from the gitignore branch and applies them to the feature branch.
It is not necessary to ever merge the gitignore branch into the main branch, because though the `git rebase` command, the `.gitignore` files are continuously updated and when a feature branch eventually is merged into the main branch, the changes made to the `.gitignore` will automatically come with it.

So, whenever a person continous to work on their feature branch, it is best practice to run the `git rebase` command to receive a updated version of the `.gitignore` file.

## 2 - Theoretical Questions
### What is a Hash-function?
A Hash-Function is a mathematical transformation that turns any data type (a file, a picture, a data frame) into a specific sequence of character (mostly numbers and letters). If the input is the same, the output string will always be identical. However, this transformation cannot be reversed, so I can't input the HASH into that function in order to "decrypt" it and get the original data as an output. A very common Hash-function is called SHA-256, which generates a 64-digit output out of any data. SHA-256 is broadly implemented nowadays as a verification tool for all kinds of programs. For example, if you download a linux-mirror from a third-party website, you make sure that it is not a hacked version by computing the hash of the downloaded file. If it matches with the SHA-256 hash published on the developers website, you can be certain that it is the original download file and not a hacked version.
Docker images, packages on PyPI and Github use SHA-256 in order to to verify the integrity and authenticity of downloaded files. GitHub commits are all identified by their hash and just a minor change will therefore also change the hash-identifier.

### Python modules, packages and scripts
A Python module is a single Python file that ends with `.py` and can be imported by other modules and scripts. They can contain functions, classes and variables. Modules are used to organize code into smaller pieces. Splitting the code into these smaller pieces makes testing, reusing and maintaining a lot easier than having all the code in one big data file.

A Python Package is a folder that contains multiple modules and a `__init__.py`, which tells python to treat that folder as a package. The purpose of a package is to group related modules together. Packages can also contain sub-packages, other folders with their own `__init__.py`.
A python script is a file with the ending `.py` that is intended be executed directly, for example through the terminal with the command `python main.py`. In a script, modules and packages are imported and run and functions are executed in a defined order. When a Python script is executed a program begins to run and while none of the tasks performed by the program, they are coordinated in the script.

### Docker Container and Volumes
Docker creates isolated environments for each application, so it acts like a small self-sustained computer itself. There are several benefits to using Docker. First and foremost, Docker containers allow programs do run consistently across different machines, because the environment inside the container does not depend on the host system. Furthermore, Docker Containers protect other programs, so when accidentally breaking the code of an application inside a docker container, all the other containers are not affected by it.
Another important advantage is, that Docker makes sharing applications very easy.  Once a Docker Image is built, it can be shared on any other machine that has Docker installed, without requiring the user to install any additional packages, libraries or anything else.
In this project, Docker is particularly useful because it ensures that our neural network code, the training environment, and all required Python packages behave exactly the same on every machine.

Docker Volumes allows data data to be stored outside of the container on the host system (usually the users computer). This is important because once a Docker Container is stopped, everything inside that Container is deleted. Therefore, Docker Volumes can store data outputs such as log files, databases or, like in our case, a trained machine learning model, persistently on the users device.
Another advantage of volumes is that they allow seamless data sharing between different containers. Two containers can read from or write to the same volume. So lets say we have a container that collects data from a temperature sensor and logs the data in real time. Simultaneously, a container that runs Grafana Dashboard can access that data and use the data to create visualizations of the temperature history.

### Virtual Environment Vs. Docker
A virtual environment only isolates Python Packages for a project. It ensures that different projects can run on different package versions without interfering with eachother. They are only used locally and can't be shared easily. Furthermore, they still depend on the Python version of the user and their operating system.
In contrast, Docker creates a completely isolated environment, with its own operating system, python version and all dependencies. A script that is run in a docker container will behave the same, regardless of the hosts operating system.
So while a virtual environment is ideal during the development phase to keep the local system clean, Docker is used to bundle that environment and make it shareable across different operating systems.

### Virtual Environment Vs. Docker
When the development of a application is completed and the code is ready to be deployed, a docker image can be created by using the `docker build .` command. This created image contains everything that is required for the application to run, including the correct Python version and all the dependencies. The docker build context contains all the files and folders inside of the `.` (or whatever folder was specified). However, not all of these files and folders are important for the docker container to work. Large dataset files, models and venv folder etc. must be excluded when creating a docker image. This can be achieved by specifying them in a `.dockerignore` file.

### Quality of a python package on PyPI
There are several indicators for the quality of a python package.
1. Number of Downloads
2. Release Frequency and Maintenance
3. Source Code is publicly available on Github: Users can check how active the project is, look at the issues and check the number of contributors


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

This implies that we have 60'000 observations for training and 10'000 for test. We can also see the dimensions of the image (which we have specifies) of 28x28 pixels and 1 for grayscale. The label variable on the other hand has 10 values (numbers 0-9). This tells us that our function has prepared the data correctly.

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
As explained above, best practice when developing a Python application, is to use a virtual environment, so that the package version used for the project do not conflict with other projects or the local host system. 
- The first step is to create a .venv folder on the local repository with `python3 -m venv .venv`.
- Then, the virtual machine must be activated with `source .venv/bin/activate` 

The next mandatory step is to install the required packages/dependencies. Since the virtual environment folder should not be versioned, we must excluded the folder in the `.dockerignore` file.  Since we had already created a .gitignore file based on the official [Python .gitignore template](https://github.com/github/gitignore/blob/main/Python.gitignore), the relevant folder is already included in the predefined ignore rules. Therefore, no additional entries are required.
Before being able to install the correct packages, check if (the newest version of) PIP is installed with  `pip version`. If not, run: ` apt install python3-pip -y`.

- Then the required packages can be installed with `pip install <packagename>`
- to create a requirements file that lists all the versions of the package use  `pip freeze > requirements.txt`
- So if later someone else has to install the correct versions of all the packages they can just run `pip install -r requirements.txt`

## 6 - Dockerization