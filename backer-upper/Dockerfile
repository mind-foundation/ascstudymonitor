# Docker service for creating mongodb
# and letsencrypt backups and pushing them
# to aws glacier.
# It must
#  - have network access to mongod
#  - mount the letsencrypt folder to /letsencrypt
#  - receive the asc-secrets.json with AWS secrets

FROM amazon/aws-cli:2.0.21

# install mongodb-org-tools
RUN echo $'[mongodb-org-4.2] \n\
name=MongoDB Repository \n\
baseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/4.2/x86_64/ \n\
gpgcheck=1 \n\
enabled=1 \n\
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc ' \
>> /etc/yum.repos.d/mongodb-org-4.2.repo

RUN yum update && \
    yum install -y crontabs mongodb-org-tools jq rsync tar xz && \
    yum clean all

VOLUME /letsencrypt

# run every day at 1:00am
RUN echo -e "0 1 * * * root bash /backer-upper.sh\n" >> /etc/crontab

ADD ./backer-upper.sh /backer-upper.sh

ENTRYPOINT ["crond", "-n"]
