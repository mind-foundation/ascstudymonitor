""" Configuration for ASC Study Monitor """

import json
import os

# makes some things faster
development = os.environ.get("FLASK_ENV", "") == "development"


def in_docker():
    """ Returns: True if running in a Docker container, else False """
    if not os.path.exists("/proc/1/cgroup"):
        # not on linux
        return False

    with open("/proc/1/cgroup", "rt") as ifh:
        return "docker" in ifh.read()


if in_docker():
    with open("/run/secrets/mendeley-secret") as f:
        env = json.load(f)
else:
    env = os.environ

mendeley_authinfo = {
    "client_id": env["MENDELEY_CLIENT_ID"],
    "client_secret": env["MENDELEY_CLIENT_SECRET"],
    "redirect_uri": env["MENDELEY_REDIRECT_URI"],
    "user": env["MENDELEY_USER"],
    "password": env["MENDELEY_PASSWORD"],
}

channel_auths = {
    "twitter": {
        "api_key": env["TWITTER_API_KEY"],
        "api_secret": env["TWITTER_API_SECRET"],
        "access_token": env["TWITTER_ACCESS_TOKEN"],
        "access_secret": env["TWITTER_ACCESS_SECRET"],
    }
}

post_secret_token = env.get("POST_SECRET_TOKEN", None)
if not development and not post_secret_token:
    raise RuntimeError("post secret token missing")


mendeley_group_id = "d9389c6c-8ab5-3b8b-86ed-33db09ca0198"

if in_docker():
    mongo_config = {
        "host": "mongo",
        "port": 27017,
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
    "file_attached",
    "id",
    "source",
    "title",
    "websites",
    "year",
    "slug",
    "keywords",
}

# document cache expiry time in seconds
cache_expires = 3600
