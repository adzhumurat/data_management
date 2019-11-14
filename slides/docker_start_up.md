# Настройка окружения для работы с помощью Docker

## Как настроить Postgres

* создать сеть *aviation_network*, в которой будут существовать наши контейнеры `docker network create -d bridge aviation_network`
* проверить, что сеть живёт - это можно сделать с помощью команды `docker network ls`
* Postgres должен где-то хранить свои данные - желательно делать это "снаружи" контейнера. Создаёте директорию для хранения данных `mkdir pg_data`. Проверьте, что директория пуста с помощью `ls pg_data`
* запустить контейнер с сервисом Postgres командой `docker run --name aviation-postgres --network aviation_network -v "$(pwd)/pg_data:/var/lib/postgresql/data" -d postgres:10-alpine`
* проверьте, что контейнер успешно запустился с помощью `docker ps`
* для доступа к Postgres нужен клиент psql. Чтобы получить доступ к контейнеру с Postgres запустим ещё контейнер с psql. Обратите внимание, что мы маунтим директорию с данными `docker run -it --rm  --network aviation_network -v "${SOURCE_DATA}/raw_data:/usr/share/raw_data" postgres:10-alpine psql -h aviation-postgres -U postgres`
* выполняем запрос для создания таблицы `CREATE TABLE ratings (userId bigint, movieId bigint, rating float(25), timestamp bigint);`
* время загрузить данные из csv-файла в вашу систему `\copy ratings FROM '/usr/share/raw_data/ratings.csv' DELIMITER ',' CSV HEADER`
* проверяем, что данные загружены успешно с помощью SQL запроса `SELECT COUNT(*) FROM ratings;`
* завершаем сеанс с помощью ctrl-D
* при повторных подключениях к контейнеру директорию с данными можно не маунтитьб запускать в виде `docker run -it --rm  --network aviation_network postgres:10-alpine psql -h aviation-postgres -U postgres`

Готово! Постгря настроена и готова к использованию

## Как настроить Mongo

* MongoDB нужна директория для хранения данных, создайте её с помощью команды `mkdir mongo_data`
* запустите контейнер с Mongo, подключив его в правильную сеть и замаунтив директорию с мета-данными Mongo и директорию с "сырыми" данными, которые нужно залить в контейнер `docker run --name aviation-mongo  --network aviation_network -v "$(pwd)/mongo_data:/data/db" -v "${SOURCE_DATA}/raw_data:/usr/share/raw_data" -d mongo:4.1.6`
* Стартуем контейнер-клиент `docker-compose --project-name data-prj -f docker-compose.yml run --rm --name env-app service-app bash`
* запускаем импорт документов `/usr/bin/mongoimport --host $APP_MONGO_HOST --port $APP_MONGO_PORT --db movie --collection tags --file /usr/share/mongo_data/tags.json`

Готово! Монга настроена и готова к использованию
