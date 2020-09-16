""" Configuration for ASC Study Monitor """

import json
import os


development = os.environ.get("ASC_ENV", "") == "development"

sentry_dsn = "https://91d6a27d4de14deba93bac991e05185f@sentry.io/1661534"
client_dist_path = "../client/dist"


def _in_docker():
    """ Returns: True if running in a Docker container """
    if not os.path.exists("/proc/1/cgroup"):
        # not on linux
        return False

    with open("/proc/1/cgroup", "rt") as ifh:
        return "docker" in ifh.read()


in_docker = _in_docker()

# load secrets from json if in docker
# or environment variables
secrets = {}
if in_docker:
    with open("/run/secrets/asc-secret") as f:
        secret = json.load(f)
        secrets.update(secret)
else:
    secrets.update(os.environ)


# mendeley infos
mendeley_authinfo = {
    "client_id": secrets["MENDELEY_CLIENT_ID"],
    "client_secret": secrets["MENDELEY_CLIENT_SECRET"],
    "redirect_uri": secrets["MENDELEY_REDIRECT_URI"],
    "user": secrets["MENDELEY_USER"],
    "password": secrets["MENDELEY_PASSWORD"],
}
mendeley_group_id = "d9389c6c-8ab5-3b8b-86ed-33db09ca0198"

# authentication for channels to post on
channel_auths = {
    "twitter": {
        "api_key": secrets["TWITTER_API_KEY"],
        "api_secret": secrets["TWITTER_API_SECRET"],
        "access_token": secrets["TWITTER_ACCESS_TOKEN"],
        "access_secret": secrets["TWITTER_ACCESS_SECRET"],
    }
}

# a secret token for trigerring posts
post_secret_token = secrets.get("POST_SECRET_TOKEN", None)
if not development and not post_secret_token:
    raise RuntimeError("post secret token missing")


# mongo db config
if in_docker:
    mongo_config = {
        "host": "mongo",
        "port": 27017,
        "username": "root",
        "password": "integration",
    }
else:
    mongo_config = {
        "host": "localhost",
        "port": 27017,
    }

mongo_db = "asc"

# fields to send on the documents endpoint
required_fields = {
    "abstract",
    "authors",
    "created",
    "disciplines",
    "fileAttached",
    "id",
    "journal",
    "keywords",
    "slug",
    "title",
    "websites",
    "year",
}
