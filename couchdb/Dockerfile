FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install -y \
    couchdb \
    netcat \
    logrotate \
    rsyslog 

RUN mkdir /var/run/couchdb
RUN chown -R couchdb:couchdb /var/run/couchdb

RUN mkdir /data
RUN chown -R couchdb:couchdb /data

# use custom configurations (mainly for bind_address config)
COPY local.ini /etc/couchdb/
RUN chown -R couchdb:couchdb /etc/couchdb

RUN touch couchdb.stdout && chown couchdb:couchdb couchdb.stdout
RUN touch couchdb.stderr && chown couchdb:couchdb couchdb.stderr

VOLUME /data

COPY create_dbs.sh .
COPY views/ /views/

COPY logrotate.conf /etc/logrotate.d/couchdb
RUN logrotate -f /etc/logrotate.d/couchdb

# update to use supervisor
COPY entrypoint.sh .
CMD sh entrypoint.sh
