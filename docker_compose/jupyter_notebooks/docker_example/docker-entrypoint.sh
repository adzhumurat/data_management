#!/bin/sh

case "$1" in
  train_model)
    python3 train.py
    ;;
  start_service)
    python3 train.py
    python3 service.py
    ;;
  *)
    exec "$@"
esac
