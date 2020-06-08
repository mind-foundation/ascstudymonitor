export FLASK_APP = ascmonitor.app:app
export SOURCE_COMMIT = $(shell git rev-parse HEAD)
SECRET_ENV = $(shell jq -r 'to_entries[] | "\(.key)=\"\(.value)\""' asc-secret.json)

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
	# not yet functional
	eval $(docker-machine env asc-studymonitor)
	docker-compose down
	docker-compose build
	docker-compose up -d
	docker logs -f $(docker ps -f name=app -q)

install-client:
	cd client && yarn install

build-client: install-client
	cd client && yarn build

flask-run: build-client
	${SECRET_ENV} FLASK_ENV="development" poetry run flask run

yarn-serve: install-client
	cd client && yarn serve