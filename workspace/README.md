## Installation instructions
First, download and install [Docker](https://www.docker.com/).
### Build the image
`docker build -t docker-babelnet .`
### Create the container from the image
`docker create --name babelnet-container -it docker-babelnet`
### To run or stop the container
`docker start babelnet-container` and `docker stop babelnet-container`
### Once the container is runing you can start a terminal and run commands with
`docker exec -it babelnet-container /bin/bash`
### To execute the experiments, run the following commands in the container's command terminal:
`cd experiments/babelnet`  
`./run.sh`
