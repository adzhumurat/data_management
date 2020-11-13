# Домашнее задание № 5.

Задание посвящено MongoDB. В рамках домашней работы необходимо:

- подключиться к Mongo из командной строки Linux и загрузить в Mongo текстовый JSON-файл `raw_data\tags.json`;
- выполнить запросы к Mongo через консоль:
    - подсчитайте число элементов в созданной коллекции tags в bd movies
    - подсчитайте число фильмов с конкретным тегом - `Adventure`
- используя группировку данных ($groupby) вывести top-3 самых распространённых тегов
- перенести запросы в файл [agg.js](https://github.com/adzhumurat/data_management/blob/master/docker_compose/data_client/app/src/agg.js)

Совет: запустите интерактивную консоль Mongo и выполните отладку запросов в консоли, а потом перенесите конструкции в agg.js.

**СПОЙЛЕР** команду для загрузки файла можно [подсмотреть тут](https://github.com/adzhumurat/workshop_docker_beginner/blob/dcb4921299c41256ee4ea4ae4e49f02c524ff0ce/slides/docker_mongo_hw.md)
