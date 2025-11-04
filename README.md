# Documentation File

To run the code, please follow the following steps:

## Cloning the github repo to local machine
- copy either the SSH or HTTPS url from github
- navigate to the folder you want to clone the repo and enter: `git clone <copied repo-url>`

## Setting up virtual environment and dependencies
- to create the virtual environment enter:  `python3 -m venv .venv`
- to start virtual environment enter: `source .venv/bin/activate`
- (if necessary install pip with: `sudo apt install python3-pip -y`)
- installing all dependencies: `pip install -r requirements.txt`

## Running the code
- to run the code enter: `python mnist_convnet.py`