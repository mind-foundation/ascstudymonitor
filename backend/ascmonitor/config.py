""" Configuration for ASC Study Monitor """

import json
import os

# makes some things faster
development = os.environ.get("FLASK_ENV", "") == "development"


def in_docker():
    """ Returns: True if running in a Docker container """
    if not os.path.exists("/proc/1/cgroup"):
        # not on linux
        return False

    with open("/proc/1/cgroup", "rt") as ifh:
        return "docker" in ifh.read()


env = os.environ
secrets = {}

if in_docker():
    with open("/run/secrets/asc-secret") as f:
        secret = json.load(f)
        secrets.update(secret)
else:
    secrets.update(env)

mendeley_authinfo = {
    "client_id": secrets["MENDELEY_CLIENT_ID"],
    "client_secret": secrets["MENDELEY_CLIENT_SECRET"],
    "redirect_uri": secrets["MENDELEY_REDIRECT_URI"],
    "user": secrets["MENDELEY_USER"],
    "password": secrets["MENDELEY_PASSWORD"],
}

channel_auths = {
    "twitter": {
        "api_key": secrets["TWITTER_API_KEY"],
        "api_secret": secrets["TWITTER_API_SECRET"],
        "access_token": secrets["TWITTER_ACCESS_TOKEN"],
        "access_secret": secrets["TWITTER_ACCESS_SECRET"],
    }
}

post_secret_token = secrets.get("POST_SECRET_TOKEN", None)
if not development and not post_secret_token:
    raise RuntimeError("post secret token missing")


mendeley_group_id = "d9389c6c-8ab5-3b8b-86ed-33db09ca0198"

if in_docker():
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
    "keywords",
    "slug",
    "source",
    "title",
    "websites",
    "year",
}
