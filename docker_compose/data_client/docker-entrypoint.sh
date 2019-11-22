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
    .venv/bin/python3 src/simple_service.py
    ;;
  jupyter)
    .venv/bin/jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root
    ;;
  *)
    exec "$@"
esac