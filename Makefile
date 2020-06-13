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
	docker-compose -f docker-compose.yaml up -d

docker-bash-backend:
	docker exec -it $$(docker ps -f name=ascstudymonitor_app -q) bash

docker-mongo:
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

build-client-dev: install-client
	cd client && yarn build:dev

mongod:
	mkdir -p ./data
	mongod --dbpath=./data

flask-run: build-client-dev
	${SECRET_ENV} FLASK_ENV="development" poetry run flask run

yarn-serve: install-client
	cd client && yarn serve

client-test-e2e: install-client
	cd client && yarn test:e2e

tmux-yarn-serve:
	tmux \
		new-session 'make mongod' \; \
		split-window 'make flask-run' \; \
		split-window 'make yarn-serve' \;

docker-backer-upper:
	docker build -t backer-upper ./backer-upper
	docker run -it \
		--network host --add-host mongo:127.0.0.1 \
		--volume ${PWD}/asc-secret.json:/run/secrets/asc-secret \
		--volume ${PWD}/etc/letsencrypt:/letsencrypt \
		--env BACKER_UPPER_DEV=1 \
		--entrypoint /bin/bash \
		backer-upper
