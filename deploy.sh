#!/bin/sh

# deploy the app

source .venv/bin/activate

pip freeze --exclude-editable > requirements.txt

deactivate

eb deploy
