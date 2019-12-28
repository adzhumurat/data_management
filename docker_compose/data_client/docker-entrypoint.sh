#!/bin/bash -e

case "$1" in
  load)
    bash load_data.sh
    ;;
  pipenv)
    pipenv install --deploy
    chmod -R 777 ./.venv
    chmod -R 777 ./.cache
    ;;
  service)
    pipenv run python3 src/simple_service.py
    ;;
  psql)
    psql -h postgres_host -U postgres
    ;;
  test)
    psql -h postgres_host -U postgres -c 'SELECT COUNT(*) as cnt FROM ratings'
    ;;
  mongo)
    /usr/bin/mongo ${APP_MONGO_HOST}:${APP_MONGO_PORT}
    ;;
  mongoimport)
    /usr/bin/mongoimport --host $APP_MONGO_HOST --port $APP_MONGO_PORT --db movie --collection tags --file /usr/share/data_store/raw_data/tags.json
    ;;
  jupyter)
    pipenv run jupyter notebook jupyter_notebooks --ip 0.0.0.0 --port 8888 --no-browser --allow-root
    ;;
  *)
    exec "$@"
esac