#!/bin/bash -e

case "$1" in
  load)
    bash load_data.sh
    ;;
  pipenv)
    pipenv install --deploy
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