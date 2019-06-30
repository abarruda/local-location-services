FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install -y \
    couchdb \
    logrotate \
    curl \
    netcat

RUN mkdir /var/run/couchdb

RUN mkdir /data

# use custom configurations (mainly for bind_address config)
COPY local.ini /etc/couchdb/

COPY views/ /views/
RUN /bin/sh /views/install_views.sh

# update to use supervisor
CMD couchdb

VOLUME /data
