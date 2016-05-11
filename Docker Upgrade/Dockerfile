FROM ubuntu:latest

RUN apt-get update \
 && apt-get install -y --no-install-recommends python-pip \
 && apt-get -y --purge autoremove \
 && rm -rf /var/lib/apt/lists/* 

RUN pip install docker-py

COPY docker-update-running /docker-update-running
RUN chmod 755 /docker-update-running

ENTRYPOINT ["/docker-update-running"]