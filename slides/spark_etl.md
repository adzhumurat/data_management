# Spark: инструмент Big data

Запускаем сборку контейнера на базе Ubuntu 18, в который будем устанавливать спарк

```shell
python3 spark_upstart.py -s build
```

Скачиваем нужные файлы Spark. Придётся набраться терпения, файлы скачиваются продолжительное время
```shell
python3 spark_upstart.py -s setup_spark
```

Запускаем выгрузку данных из Postgres
```shell
python3 spark_upstart.py -s extract
```

В результате выгрузки в директории `data/parquet` появится директория `links` - это таблица `movie.links`, которую мы выгрузили через JDBC драйвер в формат parquet.






