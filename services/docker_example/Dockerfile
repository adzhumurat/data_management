FROM morpheo/sklearn-base

WORKDIR /www/classifier

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY train.py /www/classifier/train.py
COPY service.py /www/classifier/service.py

ENTRYPOINT ["docker-entrypoint.sh"]
