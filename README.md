 [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) 
# ASC Study Monitor

 The ASC Study Monitor is a curated, freely accessible, and regularly updated database of scholarly publications concerning altered states of consciousness (ASCs).
 
### Requirements
- env.sh file with environment variables (ask team members)
- [conda](https://docs.conda.io/en/latest/)

### Installation

- `conda install poetry`
- `poetry config settings.virtualenvs.in-project true`
- `poetry install`

### Start

- `source ./env.sh`
- `export FLASK_APP='ascmonitor.app:app'`
- `export FLASK_ENV=development`
- `poetry run flask run`

##### Expose in network

- `poetry run flask run --host=0.0.0.0`

### FAQ

- _Q:_ `env.sh:2: command not found`
- _A:_ `cat env.sh | sed -e "s/^M//" > .env.sh && rm env.sh && mv .env.sh env.sh`
- _Q:_ Can the above be more concise?
- _A:_ Yes
