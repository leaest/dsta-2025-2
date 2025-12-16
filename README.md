# Documentation File

Note: This documentation is intended for Linux and macOS systems.

To run the code, please follow the steps below:

## Cloning the GithHub Repo to Local Machine
- Copy either the SSH or HTTPS url from GitHub
- Navigate to the folder you want to clone the repo and enter: `git clone <copied repo-url>`

## Setting up Virtual Environment and Dependencies
- To create the virtual environment enter:  `python3 -m venv .venv`
- To start the virtual environment enter: `source .venv/bin/activate`
- (If necessary install pip with: `sudo apt install python3-pip -y`)
- Installing all dependencies: `pip install -r requirements.txt`

## Running the Code
- To run the code enter: `python mnist_convnet.py`

## Using Docker
If you instead prefer to run the code through Docker, which ensures that it will work on any machine, install Docker Desktop from the web, enable the WSL connection inside the program under Settings > Resources > WSL Integration, if you have not already. 
Inside the github repo run the following codes:
- `docker build -t dsta-ms2 .` to build the image
- `docker run --rm dsta-ms2` to run said docker container

## Docker compose
To run the entire service created by the docker-compose file run the command:
`docker compose up` 
To force it to recreate the images you can use: `docker compose up --build` 
If you want to recreate everything from scratch (including the volumes) use:
`docker compose down -v` followed by `docker compose up`.

**pgAdmin**
View your Database via pgAdmin:
1. Once the Docker container is running, open pgAdmin in your browser: [http://localhost:8081](http://localhost:8081)
2. Log in:<br>- Email: `admin@example.com`<br>- Password: `admin`
3. Add a new server:<br>- Host: `db`<br>- Port: `5432`<br>- Username: `ms3user`<br>- Password: `ms3password`
4. On the left side follow `db_milestone3` --> `Schemas` --> `Tables`
5. Rightclick any table and select `View/Edit Data` to see its contents
