FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install -y \
	git \
    python \
    python-pip \
    nmap \
    libsnmp-dev \
    gcc \ 
    python-dev \
    net-tools \
    iputils-ping

RUN pip install python-libnmap easysnmp couchdb
RUN mkdir /scanner && cd /scanner && pip install -e git+https://github.com/coolbho3k/manuf.git#egg=manuf

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY *.py /scanner/
COPY properties.ini /scanner/

# small sleep to give db a chance to start
CMD sleep 5 && python /scanner/scanner.py /scanner/properties.ini
