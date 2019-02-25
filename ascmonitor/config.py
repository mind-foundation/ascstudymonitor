""" Configuration for ASC Study Monitor """

from datetime import timedelta
import os

mendeley = {
    'client_id': os.environ['MENDELEY_CLIENT_ID'],
    'client_secret': os.environ['MENDELEY_CLIENT_SECRET'],
    'redirect_uri': os.environ['MENDELEY_REDIRECT_URI'],
    'user': os.environ['MENDELEY_USER'],
    'password': os.environ['MENDELEY_PASSWORD'],
}

if 'RDS_HOSTNAME' in os.environ:
    # running on aws
    ascdb_uri = f"mysql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}:{os.environ['RDS_PORT']}/{os.environ['RDS_DB_NAME']}"
else:
    ascdb_uri = os.environ['ASCDB_URI']

refresh_interval = timedelta(seconds=300)
