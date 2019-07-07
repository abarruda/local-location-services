FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install -y \
    couchdb \
    logrotate 

RUN mkdir /var/run/couchdb
RUN chown -R couchdb:couchdb /var/run/couchdb

RUN mkdir /data
RUN chown -R couchdb:couchdb /data

# use custom configurations (mainly for bind_address config)
COPY local.ini /etc/couchdb/
RUN chown -R couchdb:couchdb /etc/couchdb

RUN touch couchdb.stdout && chown couchdb:couchdb couchdb.stdout
RUN touch couchdb.stderr && chown couchdb:couchdb couchdb.stderr

COPY views/ /views/
RUN /bin/sh /views/install_views.sh

# update to use supervisor
CMD su couchdb -c couchdb

VOLUME /data
