FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3-pip python3.6 python3.6-dev wget \
    openjdk-8-jre-headless ca-certificates-java \
    libffi-dev freetds-dev libkrb5-dev libsasl2-dev libssl-dev zip && \
    update-alternatives --install /usr/bin/python3 python3.6 /usr/bin/python3.6 0 && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR "/srv/spark"

ENTRYPOINT ["docker-entrypoint.sh"]
