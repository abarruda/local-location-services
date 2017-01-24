#FROM resin/rpi-raspbian:jessie

FROM locallocationservices_network-test

RUN apt-get update && apt-get install -y \
  python \
  python-pip

RUN pip install couchdb flask tornado

COPY *.py /api/
COPY properties.ini /api/

EXPOSE 80

CMD sleep 2 && python /api/ApiServer.py /api/properties.ini

