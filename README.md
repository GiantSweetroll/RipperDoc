# RipperDoc
An application to take picture of an item and can identify the nearest repair service shop related to that product.

## Docker Containers
This project makes use of Docker for containerization as well as Docker Compose. The Docker images for this project are available at [Docker Hub](https://hub.docker.com/r/giantsweetroll/ripperdoc). Docker needs to be installed in your system in order to use the images.

There are two ways to start the containers (Docker Compose or Docker run command):

### Docker Compose
1. Clone this repository at the `main` branch
2. Navigate to `ripperdoc-backend` folder an open a terminal in that location
3. In the terminal, type `docker compose up` and hit enter. This should start all of the necessary containers. The backend container service will be available at port `5000` while the serving container service will be available at port `8501`

### Using Docker run command
Open a terminal and enter the following commands
```
docker pull giantsweetroll/ripperdoc:serving
docker pull giantsweetroll/ripperdoc:backend
```
This will pull the needed images and be available for use. <br>

Nexxt, run the containers:
```
docker run -d -p 8501:8501 --name ripperdoc-serving giantsweetroll/ripperdoc:serving
docker run -d -p 5000:5000 --name ripperdoc-backend giantsweetroll/ripperdoc:backend
```
This will make the serving and backend container services available at ports `8501` and `5000` respectively. Feel free to change the port for the backend service, but do not change the port mapping for the serving service.

## Backend
The backend service is tasked in processing the image sent by the user. That image is then sent to the serving service so that the neural network model can process said image and return the name of the logo it detects from it. The result from the serving service is provided as an HTTP response from POST and GET. For a more detailed documentation regarding the API please run the backend service Docker container and go to `/docs`. For example `http://localhost:5000/docs`.
