#/bin/sh
echo "Загружаем links.csv..."
psql --host $APP_POSTGRES_HOST  -U postgres -c \
    "\\copy movie.links FROM '/usr/share/data_store/raw_data/links.csv' DELIMITER ',' CSV HEADER"

echo "Загружаем ratings.csv..."
psql --host $APP_POSTGRES_HOST -U postgres -c \
    "\\copy movie.ratings FROM '/usr/share/data_store/raw_data/ratings.csv' DELIMITER ',' CSV HEADER"

psql --host $APP_POSTGRES_HOST -U postgres -c \
    "\\copy movie.events FROM '/usr/share/data_store/raw_data/events.csv' DELIMITER ',' CSV HEADER"
