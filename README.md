# ASC Study Monitor

![Version](https://img.shields.io/badge/Version-2.0-orange)
![GitHub issues](https://img.shields.io/github/issues/membranepotential/ascstudymonitor)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/membranepotential/ascstudymonitor)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)

## Introduction

The ASC Study Monitor is a curated, freely accessible, and regularly updated database of scholarly publications concerning altered states of consciousness (ASCs).

## Todos

[Live at Github](https://github.com/membranepotential/ascstudymonitor/issues)

## Installation

- Install [conda](https://docs.conda.io/en/latest/)
- `conda install poetry`
- `poetry config settings.virtualenvs.in-project true`
- `poetry install`

## Start

- Start mongoDB
  - osx: `sudo mongod --dbpath=./data`
- `source ./env.sh`
- `export FLASK_APP='ascmonitor.app:app'`
- `export FLASK_ENV=development`
- `poetry run flask run`

#### Expose in network

- `poetry run flask run --host=0.0.0.0`
