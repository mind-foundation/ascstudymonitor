# Requirements
- env.sh file with environment variables (ask team members)
- [conda](https://docs.conda.io/en/latest/)

# Installation

- `conda install poetry`
- `poetry config settings.virtualenvs.in-project true`
- `poetry install`

# Start

- `source ./env.sh`
- `export FLASK_APP='ascmonitor.app:app'`
- `export FLASK_ENV=development`
- `poetry run flask run`

### Expose in network

- `poetry run flask run --host=0.0.0.0`

# FAQ

- _Q:_ `env.sh:2: command not found`
- _A:_ `cat env.sh | sed -e "s/^M//" > .env.sh && rm env.sh && mv .env.sh env.sh`
- _Q:_ Can the above be more concise?
- _A:_ Yes
