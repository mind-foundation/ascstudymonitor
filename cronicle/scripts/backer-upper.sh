#!/bin/bash

set -e

# prepare backup directory
timestamp=$(date -u +'%Y-%m-%dT%H:%M:%S%Z')
BACKUP_DIR="/backups/asc-studymonitor-$timestamp"
mkdir -p $BACKUP_DIR
cd $BACKUP_DIR

# load secrets
SECRETS_JSON="/run/secrets/asc-secret"
source <(jq -r 'to_entries[] | "export \(.key)=\"\(.value)\""' "$SECRETS_JSON")

# mongodump
MONGO_HOST="mongo"
MONGO_PORT="27017"
MONGO_DATABASE="asc"
MONGO_AUTH_DB="admin"
MONGO_OUTDIR="${BACKUP_DIR}/mongodb"
if [ -z "$BACKER_UPPER_DEV" ]; then
    MONGO_USERNAME="root"
    MONGO_PASSWORD="integration"
    mongodump --host=$MONGO_HOST \
              --port=$MONGO_PORT \
              --username=$MONGO_USERNAME \
              --password=$MONGO_PASSWORD \
              --db=$MONGO_DATABASE \
              --authenticationDatabase=$MONGO_AUTH_DB \
              --out="$MONGO_OUTDIR"
else
    mongodump --host=$MONGO_HOST \
              --port=$MONGO_PORT \
              --db=$MONGO_DATABASE \
              --out="$MONGO_OUTDIR"
fi

# letsencrypt
rsync -av /letsencrypt "$BACKUP_DIR"

# cronicle
rsync -av /opt/cronicle/data "$BACKUP_DIR"/cronicle_data

# prepare backup archive for upload
cd ..
BACKUP_ARCHIVE="asc-studymonitor-${timestamp}.tar.xz"
tar --force-local -cJf "$BACKUP_ARCHIVE" "$BACKUP_DIR"

# upload to aws
S3_URI="s3://asc-studymonitor-backup"
aws s3 cp "$BACKUP_ARCHIVE" "$S3_URI"

# remove archive
rm -rf "$BACKUP_DIR"
rm "$BACKUP_ARCHIVE"
