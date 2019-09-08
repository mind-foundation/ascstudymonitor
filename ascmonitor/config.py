""" Configuration for ASC Study Monitor """

import json
import os


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

mendeley_group_id = "d9389c6c-8ab5-3b8b-86ed-33db09ca0198"

if in_docker():
    redis_config = {"host": "redis", "port": 6379, "db": 0}
else:
    redis_config = {"host": "localhost", "port": 6379, "db": 0}

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
}

# document cache expiry time in seconds
cache_expires = 3600
