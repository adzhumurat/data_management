SELECT
    date,
    subsite_title,
    SUM(content_watch)::float / SUM(content_impression)::float as conversion
FROM (
    SELECT
        user_id_for_mai,
        content_id,
        subsite_title,
        to_char(to_timestamp(rocket_datetime), 'YYYY-MM-DD') as date,
        MAX(CASE WHEN name in ('page_impression', 'click') THEN 1 ELSE 0 END) as content_impression,
        MAX(CASE WHEN name='content_watch' THEN 1 ELSE 0 END) as content_watch
    FROM movie.events
    WHERE
        content_id > 0
        AND subsite_title in ('xboxOne', 'Windows 10')
    GROUP BY user_id_for_mai, content_id, date, subsite_title
) as content_watches
WHERE
    content_impression > 0
GROUP BY date, subsite_title
ORDER BY date, subsite_title