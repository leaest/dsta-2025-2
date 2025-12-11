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



