FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install -y \
    couchdb

RUN mkdir /var/run/couchdb

# use custom configurations (mainly for bind_address config)
COPY local.ini /etc/couchdb/

# update to use supervisor
CMD couchdb
