FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install -y \
  wget \
  python

# https://stackoverflow.com/a/37531821
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

RUN pip install couchdb flask tornado

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY *.py /api/
COPY properties.ini /api/

EXPOSE 80

CMD sleep 2 && python /api/ApiServer.py /api/properties.ini