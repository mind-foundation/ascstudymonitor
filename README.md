# ASC Study Monitor

![Version](https://img.shields.io/badge/Version-2.0-orange)
![GitHub issues](https://img.shields.io/github/issues/membranepotential/ascstudymonitor)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/membranepotential/ascstudymonitor)
![Client Unit Tests](https://github.com/membranepotential/ascstudymonitor/workflows/Client%20Unit%20Tests/badge.svg)
![Backend Unit Tests](https://github.com/membranepotential/ascstudymonitor/workflows/Backend%20Unit%20Tests/badge.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)

## Introduction

The ASC Study Monitor is a curated, freely accessible, and regularly updated database of scholarly publications concerning altered states of consciousness (ASCs). https://asc-studymonitor.mind-foundation.org/

## Todos

[Live at Github](https://github.com/membranepotential/ascstudymonitor/issues)

## Installation

- Install [conda](https://docs.conda.io/en/latest/)
- `conda install poetry`
- `poetry config virtualenvs.in-project true`
- `poetry install`

## Start

- Start mongoDB
  - osx: `sudo mongod --dbpath=./data`
- `make backend-run`

### Populate the database

- In the browser, navigate to exactly `http://localhost:5000/graphql/` (beware of the trailing slash)
- Run the following query:
```graphql
mutation {
  updatePublications {
    success
  }
}
```

## E2E Tests

- Start server so flask is serving at port 5000
- `cd client`
- `yarn test:e2e`
