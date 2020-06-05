export SOURCE_COMMIT = $(shell git rev-parse HEAD)

docker-dev-build:
	docker-compose -f docker-compose-dev.yaml build

docker-dev-up: docker-dev-build
	docker-compose -f docker-compose-dev.yaml up

docker-prod-build:
	docker-compose -f docker-compose.yaml build	

docker-prod-up: docker-prod-build
	docker-compose -f docker-compose.yaml up

bash-backend:
	docker exec -it $$(docker ps -f name=ascstudymonitor_app -q) bash

mongo:
	docker exec -it $$(docker ps -f name=ascstudymonitor_mongo -q) mongo -u root -p integration

deploy:
	eval $(docker-machine env asc-studymonitor)
	docker-compose down
	docker-compose build
	docker-compose up -d
	docker logs -f $(docker ps -f name=app -q)
