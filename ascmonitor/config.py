""" Configuration for ASC Study Monitor """

import os


mendeley_authinfo = {
    'client_id': os.environ['MENDELEY_CLIENT_ID'],
    'client_secret': os.environ['MENDELEY_CLIENT_SECRET'],
    'redirect_uri': os.environ['MENDELEY_REDIRECT_URI'],
    'user': os.environ['MENDELEY_USER'],
    'password': os.environ['MENDELEY_PASSWORD'],
}

mendeley_group_id = 'd9389c6c-8ab5-3b8b-86ed-33db09ca0198'

redis_config = {'host': 'localhost', 'port': 6379, 'db': 0}

# document cache expiry time in seconds
cache_expires = 300
