# Milestone 3 Report

## Task 1
If for Docker the Docker-Desktop app was installed, no installation of docker compose is necessary, since this service is included in the Docker-Desktop app.

### Necessary Services
The project introduced the getting-started[https://docs.docker.com/compose/gettingstarted/] documentation of Docker Compose uses two different services.
Docker Compose helps to control multiple services inside and between the containers. The Docker Compose file gives instructions about the services and containers. It furthermore contains configurations that are to be used for each of these services, such as which image to use, which ports are opened and how it communicates with other services.

**Web**
The Web service is a Docker container that runs a Flask application. Basically, the Web service runs the Docker image that is inside the directory and runs Flask. Flask creates a small web server inside the container. Flask listens for incoming requests of the webserver and responds based on the instructions written in the `app.py`

**Redis**
The second service is the Redis service. In the example Redis is used to retrieve the information for how often the user has opened the Website.

In Docker Compose every service gets gets a host name equal to its service name. This means that Docker Compose automatically creates a virtual network where all the containers can talk to each other using these names instead of IP-Addresses. This is possible because Docker has its own DNS-Resolver where the names are connected to the IP-Addresses of these services. This is great because even if the IP-Addresses change when the containers are recreated or someone else runs the docker compose file, since this could lead to different IP assigned to the containers. Using the hostname instead of IP addresses will ensure that the entire network will remain functional without manual configurations.

### Internal Ports
In Docker, each container has its own ports. These are usually separate from the host machine and are only visible inside Docker. This means that programs running inside a container cannot be reached from the host computer unless those ports are explicitly mapped or exposed through the Docker Compose configuration.

In the example from the "getting started" Redis runs on its default internal port 6379 inside the Redis container. This port is not exposed to the host machine because it is only meant to be accessed by other containers, not by the computer. So the The Flask application connects to Redis using the hostname redis (the service name) and port 6379.

However, not all services automatically listen on outside ports. If not defined, otherwise, Flask only accepts connections from inside its own container. Since Redis runs in its own separate container but Flask needs to be able to talk with Redis, Flask must accept communication with other containers, not just within its container. This is done with the following command inside the Dockerfile: `ENV FLASK_RUN_HOST=0.0.0.0`.
Furthermore, the Dockerfile specifies on which port to use in order to reach said container with the code `EXPOSE 5000`. This does not expose the port to the outside of the Docker network but it specifies the internal port of the container.

### External Ports
On the other hand, in the `compose.yaml` file the port of the web service are mapped in the following way: `8000:5000`. Inside the container, the port listens on port 5000 but it is made available to the outside on port 8000. So internally, other containers will still use the port 5000 to talk with the web service but if I want to visit the website with my computer (externally, since it is not in the local docker container network) the port 8000 must be used. Therefor the server can be reached by visiting `http://localhost:8000/` or `http://127.0.0.1:8000/` (with the IP of local host).

### Local Host
`localhost` is the hostname that is mapped to the own computer, it is basically the host name for the home IP address `127.0.0.1`. When opening the `http://localhost/` the browser is not connecting to the internet but to the own device.

This enables developers to test web servers and other applications locally and therefor eliminating the need exposing any ports to the internet. Moreover, as seen above, `localhost` works great with Docker since it allows to access containers through exposed ports.

The localhost also works from inside containers, since these act as "mini-computers". So when you are inside a docker container, the `localhost` refers to that container itself.


## Task 4
In Task 4 we combined the container that trained our model with various other services with the goal of having a reproducible, containerized machine learning system in which a dedicated training container that produces a model stored in a persistent model. The second container  uses that model for inference, and one of the predictions is stored in a PostgreSQL database, and it is linked via a foreign key to the corresponding input image that was used for inference. The foreign key is a mechanism in a relational database that creates a logical link between two tables, ensuring that related data stays consistent. The database can be accessed through pgAdmin.

To avoid unnecessary retraining, a model-existence check was implemented. Before starting the training process, the trainer verifies whether a trained model already exists at a predefined path inside a shared Docker volume. If the model file is present, training is skipped and the existing model is loaded instead. This ensures reproducibility, reduces startup time, and prevents redundant computation when the containers are restarted. The trained model is stored in a named Docker volume (model_data).

The application container loads the trained model from the shared volume and performs inference on input data. At the beginning I installed a sleep timer, so that if the Container couldn't find the model, it would check after 60 seconds. This step was necessary to avoid conditions during container startup, where the inference container may start before the training container has finished saving the model to the shared volume. However, an alternative solution was to make the container of the application dependent on the model container with the condition `service_completed_successfully`.

The PostgreSQL database listens on port 5432 within the Docker network and is not directly exposed to the host system, ensuring that database access is restricted to the internal services. pgAdmin is exposed via port 5050 on the host, allowing the database to be inspected and managed through a web interface. The application and training containers do not expose any ports, as they communicate exclusively through the internal Docker network.

In order to prevent errors when the application is started multiple times, the existence of the database is checked  before initialization. This  is implemented in the file `src/db_utils.py`, specifically in the function `create_database_if_not_exists()`. The function first establishes a connection to the default PostgreSQL database (postgres), which is always available, and then queries the system catalog table pg_database to check whether a database with the configured name (db_milestone3) already exists. If the query returns no result, the database is created dynamically using a `CREATE DATABASE` statement. Otherwise, the creation step is skipped and the existing database is reused.

### Conditions for the `depends_on`

**service_started**
This condition only checks whether the dependent container has started (i.e. the container process is running).
It does not guarantee that the service inside the container is ready to accept connections.

**service_healthy**
This condition ensures that the container that it depends on not only is running but it also excepts outside request. This is done with a health check, which sends a request to said container.
A service is considered healthy only if a health check is defined and that health check is passed.

**service_completed_successfully**
This condition waits until the dependent service finishes execution and exits with status code 0.
It is useful for containers that only need to be run once, such as model training.

## Explanation of the Docker Compose File

**PostgreSQL**
- The db service runs a PostgreSQL server using the official postgres:latest image.
- The database user, password, and default database are configured via the environment variables.
- Port 5432 is exposed to the host system, that allows pgAdmin to connect to the database.
- A health check is done to ensure that the PostgreSQL server is fully ready to accept connections before dependent services (such as the application container) are started.
- A Docker volume (db_data) is mounted to /var/lib/postgresql, ensuring that all database data persists even if the container is stopped or removed.

**Model Trainer**
- The trainer service builds an image from the ./modeltrainer directory and is responsible for training the neural network.
- The trained model is saved into a shared Docker volume (model_data) mounted at /app/models.
- The model is not copied into the image, ensuring that trained artifacts are not stored in Git but are instead generated.
- This design allows the training process to run once and store its output for reuse by other services.

**Application Service**
- The app service builds the inference and database interaction logic from the ./app directory.
- It depends on both the database and the trainer:
- The database must be healthy before the application starts.
- The trainer must have completed successfully, ensuring the model exists.
- Database connection parameters are passed via environment variables.
- The shared model volume is mounted in read-only mode (:ro), preventing accidental modification of the trained model.
- The application loads the trained model, stores input samples in the database, performs predictions, and saves the prediction results with foreign-key references.

**PGAdmin**
- The pgadmin service provides a web-based database administration interface.
- It depends on the PostgreSQL service.
- Default login credentials are configured via environment variables.
- pgAdmin runs its web interface inside the container on port 80 and
- Port 8081 is exposed, allowing access through http://localhost:8081.
- A dedicated volume (pgadmin_data) persists pgAdmin configuration and connection settings.
- This service is used to look at the the contents of the database.


