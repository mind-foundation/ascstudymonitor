# Simple service that keeps the document cache warm
# by curling /update every hour
# using cron

FROM alpine:3.7
RUN apk add --no-cache curl

RUN echo -e "0 * * * * curl http://app:8000/update\n" >> /etc/crontabs/root

ENTRYPOINT ["crond", "-f", "-d", "8"]
