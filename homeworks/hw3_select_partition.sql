SELECT userid, movieid, 
        ((rating 
        - MIN(rating) OVER (PARTITION BY userId))
        /(MAX(rating) OVER (PARTITION BY userId) 
        - MIN(rating) OVER (PARTITION BY userId))) as normed_rating,
        AVG(rating) OVER (PARTITION BY userId) as avg_rating
    FROM (
        SELECT DISTINCT userid, movieId, rating
            FROM movie.ratings
            WHERE userId <> 1 
            LIMIT 3000
    ) as sample
    ORDER BY userid LIMIT 30;