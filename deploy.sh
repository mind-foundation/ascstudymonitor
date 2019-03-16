#!/bin/sh

# deploy the app
poetry run pip freeze --exclude-editable > requirements.txt
eb deploy
