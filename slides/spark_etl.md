# Spark: инструмент Big data

Сначала нужно скачать архив с данными [item_views_dataset.tar.gz](https://cloud.mail.ru/public/nhpP/SyHmQQWnx).
Распаковывать архив не нужно.

Переносим архив в директорию `spark_example` этого репозитория.

Запускаем контейнер c Jupyter+Spark на борту

```shell
python3 upstart.py -s spark-jupyter
```

В консоли будет адрес, по которому ноутбук доступен в браузере

```shell
[I 16:17:16.898 NotebookApp] Jupyter Notebook 6.1.4 is running at:
[I 16:17:16.898 NotebookApp] http://c42d7716d03e:8888/?token=156ec41da4adf413887c695dac5d179c1f182bf05fda2528
[I 16:17:16.898 NotebookApp]  or http://127.0.0.1:8888/?token=156ec41da4adf413887c695dac5d179c1f182bf05fda2528
[I 16:17:16.898 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 16:17:16.902 NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/nbserver-7-open.html
    Or copy and paste one of these URLs:
        http://c42d7716d03e:8888/?token=156ec41da4adf413887c695dac5d179c1f182bf05fda2528
     or http://127.0.0.1:8888/?token=156ec41da4adf413887c695dac5d179c1f182bf05fda2528
```

Открываем в браузере страницу с интерфейсом Jupyter
```shell script
http://0.0.0.0:8890/?token=156ec41da4adf413887c695dac5d179c1f182bf05fda2528
```

Переходим в директорию `work` и открываем файл `big_data_analysys.ipynb` - там будут дальнейшие шаги для анализа.
