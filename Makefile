export SOURCE_COMMIT = $(shell git rev-parse HEAD)
SECRET_ENV = $(shell jq -r 'to_entries[] | "\(.key)=\"\(.value)\""' asc-secret.json)

docker-dev-build:
	docker-compose -f docker-compose-dev.yaml build

docker-dev-up: docker-dev-build
	docker-compose -f docker-compose-dev.yaml up

docker-prod-build:
	docker-compose -f docker-compose.yaml build	

docker-prod-up: docker-prod-build
	rm -f cronicle/logs/cronicle.pid
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

install-backend:
	cd backend && poetry install

backend-run: install-backend build-client-dev
	cd backend; \
	${SECRET_ENV} ASC_ENV="development" \
		poetry run uvicorn \
			--host 127.0.0.1 \
			--port 5000 \
			--reload \
			--access-log \
			--log-level debug \
			"ascmonitor.app:app"

yarn-serve: install-client
	cd client && yarn serve

client-test-e2e: install-client
	cd client && yarn test:e2e

tmux-yarn-serve:
	tmux \
		new-session 'make mongod' \; \
		split-window 'make backend-run' \; \
		split-window 'make yarn-serve' \;
