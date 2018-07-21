#!/bin/bash

sudo docker create --name babelnet-container -it docker-babelnet
sudo docker start babelnet-container
sudo docker exec -it babelnet-container /bin/bash