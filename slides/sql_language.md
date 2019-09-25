# Командная строка PostgreSQL

Для доступа к Postgres мы будем использовать утилиту командной строки psql. Для начала нужно

<pre>
docker-compose --project-name data-cli -f docker-compose.yml run --rm --name service-cli service-cli psql -h postgres_host -U postgres
</pre>

Если всё прошло успешно, мы увидим приглашение интерактивной сессии Postgres клиента:

<pre>
psql (10.5 (Debian 10.5-1.pgdg90+1))
Type "help" for help.

postgres=#
</pre>

Проверим, что в БД есть какие-то таблицы

<code>
SELECT
    table_schema,
    table_name
FROM information_schema.tables
LIMIT 10;
</code>


## Создание пользователя и схемы данных

Попробуем создать пользователя БД и схему данных

<pre>
CREATE USER ololouser WITH PASSWORD 'ololopass';
CREATE DATABASE ololodb;
GRANT ALL PRIVILEGES ON DATABASE ololodb TO ololouser;
</pre>

## Создание таблиц

Для создания таблицы в Postgres нужно указать типы данных для полей, а также задать ключии таблицы.

Общий шаблон создания таблиц

<pre>
CREATE TABLE table_name (
 column_name TYPE column_constraint,
 table_constraint table_constraint
)
</pre>

Конкретный пример

<pre>
CREATE TABLE
account_temp (
    user_id serial PRIMARY KEY, -- имя поля, тип данных, ограничение
    email VARCHAR (355) UNIQUE NOT NULL,
    last_login TIMESTAMP
);
</pre>

Заполняем табличку данными

<pre>
INSERT INTO account_temp VALUES (123, 'ololo@ya.ru', '2003-2-1'::timestamp);
</pre>

Производим выборку данных

<pre>
SELECT * FROM account_temp;
</pre>

Результат

<pre>
 user_id |    email    |     last_login
---------+-------------+---------------------
     123 | ololo@ya.ru | 2003-02-01 00:00:00
(1 row)

postgres=#
</pre>

Вопрос: почему ошибка?

<pre>
INSERT INTO
    account_temp
VALUES
    (1235, 'ololo@ya.ru', '2023-2-1'::timestamp),
    (1234, 'ololo123@ya.ru', '2013-2-1'::timestamp);
</pre>

Результат

<pre>
ERROR:  duplicate key value violates unique constraint "account_email_key"
DETAIL:  Key (email)=(ololo@ya.ru) already exists.
</pre>

Как добавить новую колонку
<pre>
ALTER TABLE account_temp ADD COLUMN phone VARCHAR;
</pre>

Заполнить колонку рандомными значениями
<pre>
UPDATE account_temp SET phone=md5(random()::text);
</pre>

ПРоизведём выборку данных

<pre>
SELECT * FROM account_temp;
</pre>

Результат

<pre>
 user_id |     email      |     last_login      |              phone
---------+----------------+---------------------+----------------------------------
     123 | ololo@ya.ru    | 2003-02-01 00:00:00 | 48a38b8b836d5ee6bc01d801c37129d
    1235 | ololoww@ya.ru  | 2023-02-01 00:00:00 | 74c41824f87047170e4bd7ea701d09b0
    1234 | ololo123@ya.ru | 2013-02-01 00:00:00 | f2a50425a94d4d6add1036b9b4ba4c67
(3 rows)
</pre>

# SQL

## Простые выборки

Операцию реляционной алгебры "Выборка" рeализует оператор SELECT языка SQL, параметром SELECT является имя таблицы, из которой производим выборку. Количество кортежей в выборке можно ограничить с помощью оператора LIMIT.

Выборку можно ограничить с помощью различных условий на атрибуты кортежей - эти условия(предикаты) содержаться в операторе WHERE.
Например, в качестве условия можно использовать оператор LIKE ([предикат текстовых полей](http://www.sql-tutorial.ru/ru/book_predicate_like.html))

<pre>
SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE
    table_name like '%temp%'
LIMIT 10;
</pre>

Результирующая выборка:

<pre>
 table_schema |   table_name
--------------+----------------
 public       | temp
 pg_catalog   | pg_pltemplate
 pg_catalog   | pg_ts_template
(3 rows)
</pre>


## Объединение выборок: сложение, пересечение, вычитание.

Ингда требуется достать из двух (или больше) различных таблиц данные с одинаковым набором полей - например, когда вы хотите проанализировать информацию об одном и том же процессе из двух независимых источников.

Если нужно объединить две выдачи - используем UNION (можно с модификатором UNION ALL)

<pre>
(
    SELECT
        userId,
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD') as dt
    FROM public.ratings
    WHERE
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD')='2002/09/03'
    LIMIT 2
) UNION ALL (
    SELECT
        userId,
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD') as dt
    FROM public.ratings
    WHERE
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD')='2015/09/03'
    LIMIT 2
);
</pre>

Результирующая выборка:

<pre>
 userid |     dt
--------+------------
  41615 | 2002/09/03
  41615 | 2002/09/03
  43232 | 2015/09/03
  43232 | 2015/09/03
(4 rows)
</pre>

Выборки можно пересекать, используя INTERSECT

<pre>
(
    SELECT
        userId,
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD') as dt
    FROM public.ratings
    WHERE
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD') >= '2010/09/03'
) INTERSECT (
    SELECT
        userId,
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD') as dt
    FROM public.ratings
    WHERE
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD') < '2015/09/03'
)
LIMIT 5;
</pre>

Результирующая выборка:

<pre>
 userid |     dt
--------+------------
      1 | 2015/03/09
     13 | 2012/09/27
     15 | 2012/08/26
     19 | 2011/11/15
     20 | 2013/05/02
</pre>

А можно строить разность двух выборок с помощью EXCEPT
<pre>
(
    SELECT
        userId,
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD') as dt
    FROM public.ratings
    WHERE
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD')>='2010/09/03'
) EXCEPT (
    SELECT
        userId,
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD') as dt
    FROM public.ratings
    WHERE
        to_char(to_timestamp(timestamp), 'YYYY/MM/DD')<'2015/09/03'
)
LIMIT 5;
</pre>

Результирующая выборка:

<pre>
 userid |     dt
--------+------------
      7 | 2017/02/05
     14 | 2017/02/27
     16 | 2017/01/28
     16 | 2017/01/29
     20 | 2015/09/05
(5 rows)
</pre>

Операторы UNION, INTERSECT, EXCEPT реализуют операции реляционной алгебры "объединение", "пересечение", "вычитание" соответственно.

## Сложные выборки: JOIN

Оператор JOIN позволяет соединить две или больше таблиц.

Проверим, что скрипт load_data.sh загрузил все данные корректно

<pre>
SELECT * FROM public.links LIMIT 1;
</pre>

Результат:
<pre>
 movieid | imdbid  | tmdbid
---------+---------+--------
       1 | 0114709 | 862
(1 row)
</pre>

Таблица с оценками
<pre>
SELECT * FROM public.ratings LIMIT 1;
</pre>

Результат:
<pre>
 userid | movieid | rating | timestamp
--------+---------+--------+------------
      1 |     110 |      1 | 1425941529
(1 row)
</pre>

Теперь, когда понятно что данные загружены, перейдём к оператору JOIN.

Синтаксис JOIN: указать таблицу которую присоединяем и поле, по которому происходит соединения:

<pre>
SELECT *
FROM public.links
JOIN public.ratings
    ON links.movieid=ratings.movieid
LIMIT 5;
</pre>

Результат:
<pre>
 movieid | imdbid  | tmdbid | userid | movieid | rating | timestamp
---------+---------+--------+--------+---------+--------+------------
     110 | 0112573 | 197    |      1 |     110 |      1 | 1425941529
     147 | 0112461 | 10474  |      1 |     147 |    4.5 | 1425942435
     858 | 0068646 | 238    |      1 |     858 |      5 | 1425941523
    1221 | 0071562 | 240    |      1 |    1221 |      5 | 1425941546
    1246 | 0097165 | 207    |      1 |    1246 |      5 | 1425941556
(5 rows)

</pre>

Видно, что в результирующем запросе столбцы из обеих таблиц

INNER JOIN выпиливает строки, для которых не нашлось ключа. LEFT JOIN (как и RIGHT JOIN) такие строки оставляет - например, можем выгрузить фильмы без оценок.

<pre>
SELECT *
FROM public.links
LEFT JOIN public.ratings
    ON links.movieid=ratings.movieid
WHERE ratings.movieid IS NULL
LIMIT 5;
</pre>

Результат:
<pre>
 movieid | imdbid  | tmdbid | userid | movieid | rating | timestamp
---------+---------+--------+--------+---------+--------+-----------
  110399 | 0028646 | 60438  |        |         |        |
   99899 | 0107519 | 128644 |        |         |        |
  117103 | 0069961 | 184061 |        |         |        |
  150950 | 0031406 | 133255 |        |         |        |
  124791 | 0028367 | 149955 |        |         |        |
(5 rows)
</pre>

OUTER JOIN выведет все строки, когда ключ есть хотя бы в одной таблице

Соединение двух и более таблиц происходит аналогично. Можем ещё раз присоединить эту табличку, используя alias:

<pre>
SELECT *
FROM public.links
LEFT JOIN public.ratings as r1
    ON links.movieid=r1.movieid
LEFT JOIN public.ratings as r2
    ON links.movieid=r2.movieid
WHERE
    r1.movieid > 1000
    AND r2.movieId%10=0
LIMIT 10;
</pre>

Результат:
<pre>
 movieid | imdbid  | tmdbid | userid | movieid | rating | timestamp  | userid | movieid | rating | timestamp
---------+---------+--------+--------+---------+--------+------------+--------+---------+--------+------------
   91500 | 1392170 | 70160  |      1 |   91500 |    2.5 | 1425942647 |      1 |   91500 |    2.5 | 1425942647
   91500 | 1392170 | 70160  |     15 |   91500 |    3.5 | 1346008594 |      1 |   91500 |    2.5 | 1425942647
   91500 | 1392170 | 70160  |     32 |   91500 |      5 | 1462301384 |      1 |   91500 |    2.5 | 1425942647
   91500 | 1392170 | 70160  |     41 |   91500 |      4 | 1445255260 |      1 |   91500 |    2.5 | 1425942647
   91500 | 1392170 | 70160  |     56 |   91500 |    3.5 | 1410108157 |      1 |   91500 |    2.5 | 1425942647
   91500 | 1392170 | 70160  |    111 |   91500 |      4 | 1490272853 |      1 |   91500 |    2.5 | 1425942647
   91500 | 1392170 | 70160  |    166 |   91500 |      4 | 1429711581 |      1 |   91500 |    2.5 | 1425942647
   91500 | 1392170 | 70160  |    212 |   91500 |      4 | 1362776063 |      1 |   91500 |    2.5 | 1425942647
   91500 | 1392170 | 70160  |    222 |   91500 |      1 | 1483533754 |      1 |   91500 |    2.5 | 1425942647
   91500 | 1392170 | 70160  |    231 |   91500 |      3 | 1345657110 |      1 |   91500 |    2.5 | 1425942647
(10 rows)
</pre>

Таким образом, оператор JOIN позволяет связывать друг с другом различные таблицы в базе данных по определённым полям.

## Агрегирующие функции

До сих пор мы занимались простыми выборками из БД. Для задач аналитики и машинного обучения требуется создавать на основе выборок агрегаты -
данные группируются по ключу (в качестве ключа выступает один или несколько атрибутов) и внутри каждой группы вычисляются некоторые статистики.


### SUM

Простое суммирование, в качестве аргемента принимает имя колонки

Примечание: признак должен быть числовой, иначе результаты могут быть странные

<pre>
SELECT SUM(rating) FROM public.ratings;
</pre>

Результат:
<pre>
   sum
----------
 91816043
(1 row)
</pre>

### COUNT

Простой счётчик записей. ЕСли передать модификатор DISTINCT - получим только уникальные записи

<pre>
SELECT
    COUNT(userId) as count,
    COUNT(DISTINCT userId) as count_distinct,
    COUNT(DISTINCT userId)/CAST(COUNT(userId) as float) unique_fraction
FROM public.ratings;
</pre>

Результат:
<pre>
 count  | count_distinct |  unique_fraction
--------+----------------+--------------------
 777776 |           7956 | 0.0102291662380943
(1 row)
</pre>

Несколько особенностей запроса

* несколько аггрегатов в одной строке
* использовали alias - дали имя колонке
* применили арифметическую операцию к результатам запроса (деление) - посчитали отношение уникальных userId к общему числу записей.

### AVG

AVG (AVERAGE) - вычисление среднего значения

<pre>
SELECT AVG(rating) from public.ratings;
</pre>

Результат:
<pre>
       avg
------------------
 3.52809035436088
(1 row)
</pre>

## Базовые статистики по группам: GROUP BY

Кроме расчёта статистик по всей таблице можно считать значения статистик внутри групп, с помощью аггрегирующего оператора GROUP BY:

Например, можем найти самых активных пользователей - тех, кто поставил больше всего оценок

<pre>
SELECT
    userId,
    COUNT(rating) as activity
FROM public.ratings
GROUP BY userId
ORDER BY activity DESC
LIMIT 5;
</pre>

Результат:
<pre>
 userid | activity
--------+----------
  45811 |    18276
   8659 |     9279
 270123 |     7638
 179792 |     7515
 228291 |     7410
(5 rows)
</pre>

Группировать можно по нескольким полям

<pre>
SELECT
    userId,
    to_char(to_timestamp(timestamp), 'YYYY/MM/DD') as dt,
    COUNT(rating) as activity
FROM public.ratings
GROUP BY 1,2
ORDER BY activity
DESC LIMIT 5;
</pre>

Результат:
<pre>
 userid |     dt     | activity
--------+------------+----------
 270123 | 2015/07/05 |     6663
  45811 | 2015/12/15 |     5085
  24025 | 2016/03/27 |     4946
 101276 | 2016/05/09 |     4834
 258253 | 2017/02/10 |     4227
(5 rows)
</pre>

## Фильтрация: HAVING

Аналогично WHERE оператор HAVING позволяет проводить фильтрацию. Разница том, что фильтруются поля с агрегирующими функциями

<pre>
SELECT
    userId,
    AVG(rating) as avg_rating
FROM public.ratings
GROUP BY userId
HAVING AVG(rating) < 3.5
LIMIT 5;
</pre>

Результат:
<pre>
 userid |    avg_rating
--------+------------------
   5761 | 3.41922005571031
   5468 | 1.66666666666667
   7662 | 3.26373626373626
   4326 | 3.33783783783784
   2466 |           3.4375
(5 rows)
</pre>

## Вложенность запросов

Кроме "плоских" запросов SQL позволяет строить вложенные конструкции - Common Table Expression и Subqueries.

### Обобщённые табличные выражения

Если запрос слишком сложные - логику выборки можно разделить на части.

Обобщённое табличное выражение (Common Table Expression) - возможность вынести часть логики в отдельное выражение

<pre>
WITH tmp_table
AS (
    SELECT *
    FROM public.ratings
    WHERE to_char(to_timestamp(timestamp), 'YYYY/MM/DD')<'2010/09/03'
)
SELECT
    userId,
    COUNT(to_char(to_timestamp(timestamp), 'YYYY/MM/DD')) AS dt_num
FROM tmp_table
GROUP BY userId
LIMIT 10;
</pre>

Результат:
<pre>
 userid | dt_num
--------+--------
      2 |     22
      3 |     10
      4 |     62
      5 |     26
      6 |      4
      8 |    113
      9 |     84
     10 |     13
     11 |    227
     12 |    248
(10 rows)
</pre>

### Подзапросы

Другой способ разделения логики формирования выборки - подзапросы. Подзапрос - это SELECT, результаты которого используются в другом SELECT/

<pre>
SELECT DISTINCT
    userId
FROM public.ratings
WHERE
    rating < (
            SELECT AVG(rating)
            FROM public.ratings
    )
LIMIT 5;
</pre>

Результат:
<pre>
 userid
--------
 233338
 174416
 196916
 164125
 157514
(5 rows)
</pre>

## Оконные(аналитические) функции

Оконные функции - полезный инструмент для построения сложных аналитических запросов.

Для их использования нужно задать парметры окна и функцию, которую хотим посчитать на каждом объекте внутри окна.

Простой пример - функция ROW_NUMBER(). Эта функция нумерует строки внутри окна. Пронумеруем контент для каждого пользователя в порядке убывания рейтингов.

<pre>
SELECT
  userId, movieId, rating,
  ROW_NUMBER() OVER (PARTITION BY userId ORDER BY rating DESC) as movie_rank
FROM (
    SELECT DISTINCT
        userId, movieId, rating
    FROM ratings
    WHERE userId <>1 LIMIT 1000
) as sample
ORDER BY
    userId,
    rating DESC,
    movie_rank
LIMIT 20;
</pre>

Результат:
<pre>
userid | movieid | rating | movie_rank
--------+---------+--------+------------
      2 |    1356 |      5 |          1
      2 |     339 |      5 |          2
      2 |     648 |      4 |          3
      2 |     605 |      4 |          4
      2 |    1233 |      4 |          5
      2 |    1210 |      4 |          6
      2 |     377 |      4 |          7
      2 |     260 |      4 |          8
      2 |      79 |      4 |          9
      2 |     628 |      4 |         10
      2 |      64 |      4 |         11
      2 |      58 |      3 |         12
      2 |      25 |      3 |         13
      2 |     762 |      3 |         14
</pre>

Параметры запроса:

* ROW_NUMBER - функция, которую применяем к окну
* OVER - описание окна

Описание окна содержит:
* PARTITION BY - поле (или список полей), которые описывают группу строк для применения оконной функции
* ORDER BY - поле, которое задаёт порядок записей внутри окна. Для полей внутри ORDER BY можно применять стандартные модификаторы DESC, ASC

Оконнная функция никак не меняет количество строк в выдаче, но к каждой строке добавляется полезная информация - например, про порядковый номер строки внутри окна

Названия функций обычно отражают их ссмысл. Ниже будут прриведены примеры использования и результаты запросо

### SUM()

Суммирует значения внутри окна. Посчитаем странную метрику - разделим каждое значение рейтинга на сумму всех рейтингов этого пользователя.

<pre>
SELECT userId, movieId, rating,
    rating / SUM(rating) OVER (PARTITION BY userId) as strange_rating_metric
FROM (SELECT DISTINCT userId, movieId, rating FROM ratings WHERE userId <>1 LIMIT 1000) as sample
ORDER BY userId, rating DESC
LIMIT 20;
</pre>

Результат:
<pre>
 userid | movieid | rating | strange_rating_metric
--------+---------+--------+-----------------------
      2 |     339 |      5 |    0.0684931506849315
      2 |    1356 |      5 |    0.0684931506849315
      2 |     648 |      4 |    0.0547945205479452
      2 |      64 |      4 |    0.0547945205479452
      2 |      79 |      4 |    0.0547945205479452
      2 |     260 |      4 |    0.0547945205479452
      2 |    1233 |      4 |    0.0547945205479452
      2 |    1210 |      4 |    0.0547945205479452
      2 |     377 |      4 |    0.0547945205479452
      2 |     605 |      4 |    0.0547945205479452
      2 |     628 |      4 |    0.0547945205479452
      2 |     762 |      3 |    0.0410958904109589
      2 |     141 |      3 |    0.0410958904109589
      2 |     780 |      3 |    0.0410958904109589
      2 |       5 |      3 |    0.0410958904109589
      2 |      58 |      3 |    0.0410958904109589
      2 |      25 |      3 |    0.0410958904109589
      2 |    1475 |      3 |    0.0410958904109589
      2 |      32 |      2 |    0.0273972602739726
      2 |    1552 |      2 |    0.0273972602739726
(20 rows)
</pre>

### COUNT(), AVG()

Счётчик элементов внутри окна, а так же функция Average(). Для наглядности воспользуемся ими одновременно - результаты не должны отличаться.
Вычислим полезную метрику - отклонение рейтинга пользователя от среднего рейтинга, который он склонен выставлять

<pre>
SELECT userId, movieId, rating,
    rating - AVG(rating) OVER (PARTITION BY userId) rating_deviance_simplex,
    rating - SUM(rating) OVER (PARTITION BY userId) /COUNT(rating) OVER (PARTITION BY userId) as rating_deviance_complex
FROM (SELECT DISTINCT userId, movieId, rating FROM ratings WHERE userId <>1 LIMIT 1000) as sample
ORDER BY userId, rating DESC
LIMIT 20;
</pre>

Результат:
<pre>
 userid | movieid | rating | rating_deviance_simplex | rating_deviance_complex
--------+---------+--------+-------------------------+-------------------------
      2 |     339 |      5 |        1.68181818181818 |        1.68181818181818
      2 |    1356 |      5 |        1.68181818181818 |        1.68181818181818
      2 |     648 |      4 |       0.681818181818182 |       0.681818181818182
      2 |      64 |      4 |       0.681818181818182 |       0.681818181818182
      2 |      79 |      4 |       0.681818181818182 |       0.681818181818182
      2 |     260 |      4 |       0.681818181818182 |       0.681818181818182
      2 |    1233 |      4 |       0.681818181818182 |       0.681818181818182
      2 |    1210 |      4 |       0.681818181818182 |       0.681818181818182
      2 |     377 |      4 |       0.681818181818182 |       0.681818181818182
      2 |     605 |      4 |       0.681818181818182 |       0.681818181818182
      2 |     628 |      4 |       0.681818181818182 |       0.681818181818182

</pre>

### MIN(), MAX()

<pre>
SELECT userId, movieId, rating,
    (rating - MIN(rating) OVER (PARTITION BY userId))/(MAX(rating) OVER (PARTITION BY userId)) rating_deviance_simplex
FROM (
    SELECT DISTINCT
        userId, movieId, rating
    FROM ratings
    WHERE userId <> 1 LIMIT 1000
) as sample
ORDER BY userId, rating DESC LIMIT 20;
</pre>

Результат:
<pre>
 userid | movieid | rating | rating_deviance_simplex
--------+---------+--------+-------------------------
      2 |     339 |      5 |                       1
      2 |    1356 |      5 |                       1
      2 |     648 |      4 |                    0.75
      2 |      64 |      4 |                    0.75
      2 |      79 |      4 |                    0.75
      2 |     260 |      4 |                    0.75
      2 |    1233 |      4 |                    0.75
      2 |    1210 |      4 |                    0.75
      2 |     377 |      4 |                    0.75
      2 |     605 |      4 |                    0.75
      2 |     628 |      4 |                    0.75
      2 |     762 |      3 |                     0.5
      2 |     141 |      3 |                     0.5
      2 |     780 |      3 |                     0.5

</pre>

### RANK(), DENSE_RANK(), PERCENT_RANK()

Ранжирующие функции - это RowNumber() "на стероидах". Различия возникают на одинаковых строках: Rank строит индекс таких строк с разрывами (gap),
а Dense_Rank без разрывов (плотный). Percent_rank конвертирует нормера строк в значение перцентилей

<pre>
SELECT userId, movieId, rating,
    RANK() OVER (PARTITION BY userId ORDER BY RATING) r_rank,
    DENSE_RANK() OVER (PARTITION BY userId ORDER BY RATING) r_rank_dense,
    PERCENT_RANK() OVER (PARTITION BY userId ORDER BY RATING)
FROM (SELECT DISTINCT userId, movieId, rating FROM ratings WHERE userId <>1 LIMIT 1000) as sample
ORDER BY userId, rating ASC
LIMIT 15;
</pre>

Результат:
<pre>
 userid | movieid | rating | r_rank | r_rank_dense |    percent_rank
--------+---------+--------+--------+--------------+--------------------
      2 |     786 |      1 |      1 |            1 |                  0
      2 |     788 |      1 |      1 |            1 |                  0
      2 |    1552 |      2 |      3 |            2 | 0.0952380952380952
      2 |      32 |      2 |      3 |            2 | 0.0952380952380952
      2 |       5 |      3 |      5 |            3 |   0.19047619047619
      2 |      58 |      3 |      5 |            3 |   0.19047619047619
      2 |     762 |      3 |      5 |            3 |   0.19047619047619
      2 |    1475 |      3 |      5 |            3 |   0.19047619047619
      2 |      25 |      3 |      5 |            3 |   0.19047619047619
      2 |     141 |      3 |      5 |            3 |   0.19047619047619
      2 |     780 |      3 |      5 |            3 |   0.19047619047619
      2 |    1210 |      4 |     12 |            4 |  0.523809523809524
      2 |      64 |      4 |     12 |            4 |  0.523809523809524
      2 |     605 |      4 |     12 |            4 |  0.523809523809524
</pre>

### FIRST_VALUE(), LAST_VALUE(), NTH_VALUE, LAG()

Функции, которые находят значение из другой строки внутри окна.

* first_value - первое значение в окне
* last_value - крайнее значение в окне
* nth_value - элемент окна под номером n
* lag - вычисляет для каждой строки смещение

<pre>
SELECT userId, movieId, rating,
    FIRST_VALUE(movieId) OVER (PARTITION BY userId ORDER BY RATING) top_content,
    last_value(movieId) OVER (PARTITION BY userId ORDER BY RATING) bottom_content,
    nth_value(movieId, 5) OVER (PARTITION BY userId ORDER BY RATING) r_nth,
    lag(movieId, 5) OVER (PARTITION BY userId ORDER BY RATING) r_lag
FROM (SELECT DISTINCT userId, movieId, rating FROM ratings WHERE userId <>1 LIMIT 1000) as sample
ORDER BY userId, rating ASC
LIMIT 15;
</pre>

Результат:
<pre>
 userid | movieid | rating | top_content | bottom_content | r_nth | r_lag
--------+---------+--------+-------------+----------------+-------+-------
      2 |     786 |      1 |         786 |            788 |       |
      2 |     788 |      1 |         786 |            788 |       |
      2 |    1552 |      2 |         786 |             32 |       |
      2 |      32 |      2 |         786 |             32 |       |
      2 |       5 |      3 |         786 |            780 |     5 |
      2 |      58 |      3 |         786 |            780 |     5 |   786
      2 |     762 |      3 |         786 |            780 |     5 |   788
      2 |    1475 |      3 |         786 |            780 |     5 |  1552
      2 |      25 |      3 |         786 |            780 |     5 |    32
      2 |     141 |      3 |         786 |            780 |     5 |     5
      2 |     780 |      3 |         786 |            780 |     5 |    58
      2 |    1210 |      4 |         786 |            377 |     5 |   762
      2 |      64 |      4 |         786 |            377 |     5 |  1475
      2 |     605 |      4 |         786 |            377 |     5 |    25
      2 |     648 |      4 |         786 |            377 |     5 |   141
(15 rows)
</pre>

Аналитические функции - супер-мощная штука. С их помощью можно делать крутой препроцессинг данных и эффективно готовить данные для моделей более высогого уровня.

