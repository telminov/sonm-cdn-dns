# docker build -t telminov/sonm-cdn-dns .
# docker push telminov/sonm-cdn-dns
FROM ubuntu:18.04

RUN apt-get clean && apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    wget git


ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . /opt/app
WORKDIR /opt/app


#EXPOSE 8053/tcp
EXPOSE 8053/udp

CMD cp /conf/settings.py .; python3 dns.py