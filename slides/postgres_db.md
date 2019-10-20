# Типы данных

## Массивы

Пример создания массива

<pre>
-- создаем таблицу, у которой значения являются массивами
CREATE TABLE holiday_picnic (
     holiday varchar(50) -- строковое значение
     sandwich text[], -- массив
     side text[] [], -- многомерный массив
     dessert text ARRAY, -- массив
     beverage text ARRAY[4] -- массив из 4-х элементов
);

 -- вставляем значения массивов в таблицу
INSERT INTO holiday_picnic VALUES
     ('Labor Day',
     '{"roast beef","veggie","turkey"}',
     '{
        {"potato salad","green salad"},
        {"chips","crackers"}
     }',
     '{"fruit cocktail","berry pie","ice cream"}',
     '{"soda","juice","beer","water"}'
     );
</pre>


## Геометрические типы данных

Есть много встроенных типов данных


 Name   |   Storage Size   |   Representation   |   Description
 ------ | ---------------- | ------------------ | -------------
 point | 16 bytes | Point on a plane | (x,y)
 line	| 32 bytes | Infinite line (not fully implemented) | 	((x1,y1),(x2,y2))
 lseg | 32 bytes | Finite line segment | 	((x1,y1),(x2,y2))
 box | 32 bytes	| Rectangular box | ((x1,y1),(x2,y2))
 path | 	16+16n bytes	| Closed path (similar to polygon) | ((x1,y1),...)
 path | 	16+16n bytes	| Open path | [(x1,y1),...]
 polygon | 40+16n	| Polygon (similar to closed path)  | ((x1,y1),...)
 circle | 24 bytes	| Circle	 |  <(x,y),r> (center point and radius)


Пример, зачем это нужно: https://habr.com/post/245015/

## Перечислимый тип

Хранить более эффективно, чем в виде строк

<pre>
CREATE TYPE week AS ENUM ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun');
</pre>


# Полезные команды psql

## Размер БД

Кооманда pg_database_size вычисляет размер БД в байтах

<pre>
SELECT pg_size_pretty(pg_database_size(current_database()));
</pre>

Результат

<pre>
 pg_size_pretty
----------------
 3000 MB
(1 row)

</pre>

## Пользовательские таблицы

Команда формирует список таблиц, которые были созданы пользователем

<pre>
SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog');
</pre>

Результат:

<pre>
 table_name
------------
 links
 ratings
(2 rows)
</pre>

Описание таблицы можно получить при помощи команды \d

<pre>
\d ratings
</pre>

Результат:

<pre>
                    Table "public.ratings"
  Column   |       Type       | Collation | Nullable | Default
-----------+------------------+-----------+----------+---------
 userid    | bigint           |           |          |
 movieid   | bigint           |           |          |
 rating    | double precision |           |          |
 timestamp | bigint           |           |          |

</pre>

Можно узнать размер таблицы

<pre>
SELECT pg_size_pretty(pg_relation_size('ratings'));
</pre>

Результат:

<pre>
 pg_size_pretty
----------------
 2990 MB
(1 row)
</pre>

Или полный размер данных (вместе с инднксами и т.д.)

<pre>
SELECT pg_size_pretty(pg_total_relation_size('ratings'));
</pre>

Результат:

<pre>
 pg_size_pretty
----------------
 2991 MB
(1 row)
</pre>

Размер данных в конкретном столбце

<pre>
SELECT pg_size_pretty(SUM(pg_column_size(userId))) FROM ratings;
</pre>

Результат:

<pre>
 pg_size_pretty
----------------
 397 MB
(1 row)
</pre>

## Администрирование и мониторинг

Запрос, который выводит информацию об активных запросах.

<pre>
SELECT
    pid,
    age(query_start, clock_timestamp()),
    usename, query, backend_type
FROM pg_stat_activity
WHERE
    query != '<IDLE>'
    AND query NOT ILIKE '%pg_stat_activity%';
</pre>

Результат:

<pre>
 pid | age | usename  | query |    backend_type
-----+-----+----------+-------+---------------------
  66 |     |          |       | autovacuum launcher
  68 |     | postgres |       | background worker
  64 |     |          |       | background writer
  63 |     |          |       | checkpointer
  65 |     |          |       | walwriter
(5 rows)
</pre>


Если запрос висит слишком долго, его стоит прибить командой

<pre>
SELECT pg_terminate_backend(procpid);
</pre>

С помощью команды \timing можно определить время выполнения запроса

<pre>
\timing
</pre>

Результат:

<pre>
Timing is on.
</pre>

Сформируем запрос:

<pre>
SELECT
    movieId,
    COUNT(*) num_rating
FROM public.ratings
WHERE
    ratings.movieID > 100000
GROUP BY 1
LIMIT 10;
</pre>

Результат:

<pre>
 movieid | num_rating
---------+------------
  100001 |          2
  100003 |          6
  100006 |          6
  100008 |         28
  100010 |         88
  100013 |         18
  100015 |          4
  100017 |         50
  100032 |         30
  100034 |         64
(10 rows)

Time: 1494.318 ms (00:01.494)
</pre>

## Ускорение запросов: индексы

Ускорить запрос можно с помощью создания индексов. Индексы можно создавать на лету

<pre>
CREATE INDEX ON ratings(movieId);
</pre>

Результат:

<pre>
Time: 37427.672 ms (00:37.428)
</pre>

После того, как индекс создан - запросы начинают выполнятся бодрее, время сокращается в сотни раз
<pre>
CREATE INDEX ON ratings(movieId);
</pre>

Результат:

<pre>
CREATE INDEX
Time: 38493.878 ms (00:38.494)
</pre>

Выполним запрос ещё раз:

<pre>
SELECT
    movieId,
    COUNT(*) num_rating
FROM public.ratings
WHERE
    ratings.movieID > 100000
GROUP BY 1
LIMIT 10;
</pre>

Результат:

<pre>
 movieid | num_rating
---------+------------
  100001 |          2
  100003 |          6
  100006 |          6
  100008 |         28
  100010 |         88
  100013 |         18
  100015 |          4
  100017 |         50
  100032 |         30
  100034 |         64
(10 rows)

Time: 5.289 ms
</pre>

## Хранимые процедуры

Хранимые процедуры - это функции, которые определяются пользователем. Их можно создавать  для более гибкого препроцессинга данных.

<pre>
CREATE OR REPLACE FUNCTION
    imdb_url(imdb_id VARCHAR)
RETURNS VARCHAR AS
$$
    BEGIN RETURN
        CONCAT(
            CAST('http://www.imdb.com/' as VARCHAR), CAST(imdb_id as VARCHAR)
        ) ;
    END;
$$
LANGUAGE plpgsql;
</pre>

Результат:

<pre>
CREATE FUNCTION
Time: 3.637 ms
</pre>

Применяем функцию:

<pre>
SELECT imdb_url(links.imdbId) FROM public.links LIMIT 10;
</pre>

Результат:

<pre>
          imdb_url
-----------------------------
 http://www.imdb.com/0114709
 http://www.imdb.com/0113497
 http://www.imdb.com/0113228
 http://www.imdb.com/0114885
 http://www.imdb.com/0113041
 http://www.imdb.com/0113277
 http://www.imdb.com/0114319
 http://www.imdb.com/0112302
 http://www.imdb.com/0114576
 http://www.imdb.com/0113189
(10 rows)

Time: 1.478 ms
</pre>

Мы создали хранимую процедуру, в которой приклеиваем к id оставшуюся часть URL. Хранимые процедуры можно делать и более сложными и использовать их  для препроцессинга данных, или внутри триггеров.

## Схема запроса

Оператор EXPLAIN демострирует этапы выполнения запроса и может быть использован для оптимизации.

<pre>
EXPLAIN
SELECT
    userId, COUNT(*) num_rating
FROM public.links
LEFT JOIN public.ratings
    ON links.movieid=ratings.movieid
GROUP BY 1
LIMIT 10;
</pre>

Результат:

<pre>
                                      QUERY PLAN
--------------------------------------------------------------------------------------
 Limit  (cost=1880431.03..1880431.13 rows=10 width=16)
   ->  HashAggregate  (cost=1880431.03..1880749.83 rows=31880 width=16)
         Group Key: ratings.userid
         ->  Hash Right Join  (cost=1323.47..1620188.15 rows=52048576 width=8)
               Hash Cond: (ratings.movieid = links.movieid)
               ->  Seq Scan on ratings  (cost=0.00..903196.76 rows=52048576 width=16)
               ->  Hash  (cost=750.43..750.43 rows=45843 width=8)

</pre>


## Data import/export

ETL (Extract, Transform, Load) - общее название для процессов загрузки сырых данных в БД, а так же выгрузки результатов для дальнейшего использования.
Для импорта и экспорта данных используется команда copy.

### Загрузка данных.

Загружать данные в Postgres можно из CSV файлов, ниже пример который загружает данные из csv:

На первом этапе создаём табличку с данными

<pre>
psql -c '
  CREATE TABLE IF NOT EXISTS ratings (
    userId bigint,
    movieId bigint,
    rating float(25),
    timestamp bigint
  );'
</pre>

И на втором этапе заливаем CSV в созданную таблицу:

<pre>
psql -c "\\copy ratings FROM '/data/ratings.csv' DELIMITER ',' CSV HEADER"
</pre>

Примечание: перед тем, как загружать данные, нужно очень внимательно изучить csv файл - чтобы точно узнать типы данных и их размерности

### Выгрузка данных

Выгрузку данных можно производить с помощью команды copy

<pre>
\copy (SELECT * FROM ratings LIMIT 100) TO 'ratings_file.csv' WITH CSV HEADER DELIMITER as ',';
</pre>

ETL процессы позволяют использовать Postgres (или другие БД) как средство вычисления: получаем данные, обрабатываем внутри Postgres используя мощный движок вычислений и выгружаем результат для дальнейшего использования - например, в алгоритмах машинного обучения.


### Дамп базы данных

Дамп - это сохранение состояния базы в текстовом виде.

Используется в качестве чекпоинта (точки восстановления) базы.

Для создания дампов в Postgres используется утилита [pg_dump](https://postgrespro.ru/docs/postgresql/9.6/app-pgdump)

<pre>
pg_dump -h $APP_POSTGRES_HOST -U postgres -t ratings_parted > ratings_parted_dump.sql
</pre>


Восстановление из дампа происходит аналогично

<pre>
psql -h $APP_POSTGRES_HOST -U postgres dbname < ratings_parted_dump.sql
</pre>

В промышленных системах дамп базы - это регулярная задача, требующая автоматизации.

## Шардирование данных

Шардинг (иногда шардирование) — техника работы с данными, суть которой в разделении (партиционирование) данных на
отдельные части (по отдельным серверам или отдельным таблицам)

Создаём партиционированную таблицу с рейтингами

<pre>
CREATE TABLE ratings_parted (
    userId bigint,
    movieId bigint,
    rating float(25),
    timestamp bigint
);
</pre>

Создаём шард -табличку с ограничениями на одно из полей - ключ шарда.

<pre>
CREATE TABLE ratings_parted_0 (
    CHECK ( userId % 10 = 0 )
) INHERITS (ratings_parted);
</pre>

Чтобы заливка происходила правильно, нужно создать дополнительное правило-триггер
<pre>
CREATE RULE ratings_insert_0 AS ON INSERT TO ratings_parted
WHERE ( userId % 10 = 0 )
DO INSTEAD INSERT INTO ratings_parted_0 VALUES ( NEW.* );
</pre>

Проверим, как все работает
<pre>
INSERT INTO ratings_parted (
    SELECT *
    FROM ratings
    WHERE userid=10
);
</pre>

Проверяем результат
<pre>
SELECT COUNT (*)
FROM ratings_parted
</pre>


Ещё одна проверка
<pre>
SELECT COUNT (*)
FROM ratings_parted_0
</pre>

Загадка: что будет, если выполнить запрос
<pre>
INSERT INTO ratings_parted (
    SELECT *
    FROM ratings
    WHERE userid=11
);
</pre>

Аналогичным образом таблицы можно разнести по разным инстансам БД.