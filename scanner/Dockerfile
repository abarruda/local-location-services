FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install -y \
    python \
    python-pip \
    nmap \
    net-tools \
    iputils-ping

RUN pip install python-libnmap couchdb

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY *.py /scanner/
COPY properties.ini /scanner/

# small sleep to give db a chance to start
CMD sleep 5 && python /scanner/scanner.py /scanner/properties.ini
