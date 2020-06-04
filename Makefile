export SOURCE_COMMIT = $(shell git rev-parse HEAD)

docker-dev-build:
	docker-compose -f docker-compose-dev.yaml build

docker-dev-up: docker-dev-build
	docker-compose -f docker-compose-dev.yaml up

docker-build:
	docker build -t ascstudymonitor .

docker-bash: docker-build
	docker run -it -v $$PWD/asc-secret.json:/run/secrets/asc-secret --add-host mongo:127.0.0.1 --network=host ascstudymonitor bash

docker-dev-run: docker-build
	docker run -it -v $$PWD/asc-secret.json:/run/secrets/asc-secret --add-host mongo:127.0.0.1 --network=host ascstudymonitor

deploy:
	eval $(docker-machine env asc-studymonitor)
	docker-compose down
	docker-compose build
	docker-compose up -d
	docker logs -f $(docker ps -f name=app -q)
