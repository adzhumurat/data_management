-- Запрос на удаление создаваемых таблиц, если они уже есть
DROP TABLE IF EXISTS movie.content_genres;
DROP TABLE IF EXISTS movie.top_rated_tags;

-- Запрос на создание таблицы 'content_genres'
CREATE TABLE movie.content_genres
(
    movieid BIGINT,
    genre VARCHAR(128)
);

-- Команда на загрузку данных в таблицу 'content_genres'
\COPY movie.content_genres FROM '/usr/share/data_store/raw_data/genres.csv' DELIMITER ',' CSV HEADER;

-- Запрос на вывод данных тыблицы 'content_genres'
select * from movie.content_genres limit 100;

-- Запрос 1
SELECT movieid, avg_rating
    FROM (
        SELECT movieid, AVG(rating) as avg_rating, COUNT(userid) as count_users
            FROM movie.ratings
            GROUP BY movieid
    ) as sample
    WHERE count_users > 50
    ORDER BY avg_rating DESC, movieid 
    LIMIT 150;

-- Запрос на получение временной таблицы
WITH top_rated as (
    SELECT movieid, avg_rating
    FROM (
        SELECT movieid, AVG(rating) as avg_rating, COUNT(userid) as count_users
            FROM movie.ratings
            GROUP BY movieid
    ) as sample
    WHERE count_users > 50
    ORDER BY avg_rating DESC, movieid 
    LIMIT 150
)

-- Запрос на заполнение таблицы 'top_rated_tags'
SELECT tr.movieid, tr.avg_rating, cg.genre 
    INTO movie.top_rated_tags
    FROM top_rated AS tr
    LEFT JOIN movie.content_genres AS cg ON cg.movieid = tr.movieid
    ORDER BY tr.avg_rating DESC;
    
-- Зарос на вывод данных 'top_rated_tags'
SELECT * FROM movie.top_rated_tags ORDER BY avg_rating DESC;

-- анды выгрузки данных в csv

\COPY (SELECT * FROM movie.top_rated_tags) TO '/usr/share/data_store/raw_data/top_rated_tags.csv' WITH CSV HEADER DELIMITER AS E'\t';

