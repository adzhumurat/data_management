FROM ubuntu:18.04

# сборка контейнера: docker build -t aviation_data_client:latest .
# запуск
# подключение в sh: docker run --volume $(pwd)/app:/www/app --network aviation_network -it --rm aviation_data_client:latest bash
# загрузка данных docker run -v $(pwd)/app:/www/app -v ${SOURCE_DATA}/raw_data:/usr/share/raw_data -e APP_POSTGRES_HOST=aviation-postgres  --network aviation_network -it --rm aviation_data_client:latest load
# подключение к postgres: docker run --volume $(pwd)/app:/www/app --network aviation_network -it --rm aviation_data_client:latest psql -h aviation-postgres -U postgres
# сборка pipenv:    docker run --volume $(pwd)/app:/www/app --network aviation_network -it --rm aviation_data_client:latest pipenv
# старт http сервера docker run -v $(pwd)/app:/www/app --network aviation_network -p 5001:5000 -d --rm aviation_data_client:latest service
# для docker-compose
# сборка docker-compose --project-name data-cli -f docker-compose.yml build service-cli
# данные docker-compose --project-name data-cli -f docker-compose.yml run --rm --name service-cli service-cli load
# клиент docker-compose --project-name data-cli -f docker-compose.yml run --rm --name service-cli service-cli psql -h postgres_host -U postgres

RUN apt-get update && \
    apt-get install -y curl nano python3-pip python3.6 python3.6-dev wget && \
    update-alternatives --install /usr/bin/python3 python3.6 /usr/bin/python3.6 0 && \
    pip3 install pipenv && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" > /etc/apt/sources.list.d/pgdg.list  && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get install -y postgresql-client-10 mongodb mongo-tools

ENV \
    # Настройка pipenv
    PIPENV_VENV_IN_PROJECT=1 \
    PIPENV_CACHE_DIR=/www/app/.cache/pipenv \
    PIP_CACHE_DIR=/www/app/.cache/pip \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

WORKDIR "/www/app"

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]