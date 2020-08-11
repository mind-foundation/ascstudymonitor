FROM bluet/cronicle-docker:latest

# install mongodb-org-tools
RUN apk add --no-cache mongodb-tools aws-cli jq rsync tar xz

VOLUME /letsencrypt

# inherited
ENTRYPOINT ["/sbin/tini", "--"]
CMD        ["sh", "/entrypoint.sh"]

