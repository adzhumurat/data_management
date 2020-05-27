#!/bin/bash -e

case "$1" in
  setup_spark)
    echo "Начинаем установку Spark"
    cd /tmp && \
    wget -q http://mirror.linux-ia64.org/apache/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.6.tgz && \
    tar xvf spark-2.4.5-bin-hadoop2.6.tgz -C /tmp/data && \
    rm spark-2.4.5-bin-hadoop2.6.tgz && \
    mv /tmp/data/spark-2.4.5-bin-hadoop2.6 /tmp/data/spark2.4
    echo "Закончили установку Spark"
    wget https://jdbc.postgresql.org/download/postgresql-42.2.12.jar && \
    mkdir -p /tmp/data/jars && \
    ls
    mv postgresql-42.2.12.jar /tmp/data/jars && \
    cp /tmp/data/conf/lo4j.properties /tmp/data/spark2.4/conf/lo4j.properties
    echo "Закончили установку jdbc Postgres коннектора"
    ;;
  pyspark)
    exec /tmp/data/spark2.4/bin/pyspark
    ;;
  extract)
    $SPARK_HOME/bin/spark-submit --packages org.postgresql:postgresql:9.4.1211 /tmp/data/scripts/extract.py
    ;;
  transform)
    $SPARK_HOME/bin/spark-submit --packages org.postgresql:postgresql:9.4.1211 /tmp/data/scripts/transform.py
    ;;
  *)
    exec "$@"
    ;;
esac
