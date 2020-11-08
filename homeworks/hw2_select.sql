SELECT 'ФИО: Насыбуллин А. А.';

-- Запрос №1.1
SELECT * 
    FROM movie.ratings 
    LIMIT 10;

-- Запрос №1.2
SELECT * 
    FROM movie.links
    WHERE 
        imdbid LIKE '%42' 
        AND movieid > 100 
        AND movieid < 1000;

-- Запрос №2.1
SELECT imdbid 
    FROM movie.links
    INNER JOIN movie.ratings 
        ON movie.ratings.movieid = movie.links.movieid
    WHERE 
        movie.ratings.rating = 5
    LIMIT 10;

-- Запрос №3.1.
SELECT DISTINCT COUNT(*)
    FROM movie.links lnk
    LEFT JOIN movie.ratings rtg
        ON rtg.movieid = lnk.movieid
    WHERE rtg.movieid IS NULL

-- Запрос №3.2
SELECT userid, AVG(rating) AS avg_ratings 
    FROM movie.ratings
    GROUP BY userid 
    HAVING 
        AVG(rating) > 3.5
    ORDER BY avg_ratings DESC
    LIMIT 10;

-- Запрос №4.1
SELECT imdbid
    FROM movie.links
    WHERE 
        movieid IN (
            SELECT movieid
                FROM movie.ratings
                GROUP BY movieid
                HAVING 
                    AVG(rating) > 3.5
                LIMIT 10
    );

-- Запрос №4.2
WITH user_ratings_more_10 AS (
    SELECT AVG(rating) AS avg_rating
        FROM movie.ratings
        GROUP BY userid
        HAVING 
            COUNT(rating) > 10
)

SELECT AVG(avg_rating)
    FROM user_ratings_more_10

