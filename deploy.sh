#!/bin/sh

# deploy the app
eval $(docker-machine env asc-studymonitor)
docker-compose down
docker-compose build
docker-compose up -d
docker logs -f $(docker ps -f name=app -q)
