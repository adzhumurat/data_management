#/bin/sh

psql --host $APP_POSTGRES_HOST  -U postgres -c \
    "DROP TABLE IF EXISTS links"
psql --host $APP_POSTGRES_HOST  -U postgres -c \
    "DROP TABLE IF EXISTS ratings"

echo "Загружаем links.csv..."
psql --host $APP_POSTGRES_HOST -U postgres -c '
  CREATE TABLE links (
    movieId bigint,
    imdbId varchar(20),
    tmdbId varchar(20)
  );'

psql --host $APP_POSTGRES_HOST  -U postgres -c \
    "\\copy links FROM '/usr/share/raw_data/links.csv' DELIMITER ',' CSV HEADER"

echo "Загружаем ratings.csv..."
psql --host $APP_POSTGRES_HOST -U postgres -c '
  CREATE TABLE ratings (
    userId bigint,
    movieId bigint,
    rating float(25),
    timestamp bigint
  );'

psql --host $APP_POSTGRES_HOST -U postgres -c \
    "\\copy ratings FROM '/usr/share/raw_data/ratings.csv' DELIMITER ',' CSV HEADER"
