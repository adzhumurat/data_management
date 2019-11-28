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
  jupyter)
    pipenv run jupyter notebook jupyter_notebooks --ip 0.0.0.0 --port 8888 --no-browser --allow-root
    ;;
  *)
    exec "$@"
esac