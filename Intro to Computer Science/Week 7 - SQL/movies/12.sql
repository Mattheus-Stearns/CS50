SELECT title
FROM movies
WHERE id IN (
    SELECT movie_id
    FROM stars
    WHERE person_id IN (
        SELECT id
        FROM people
        WHERE name = 'Jennifer Lawrence'
        OR name = 'Bradley Cooper' 
    )
    GROUP BY movie_id
    HAVING COUNT(DISTINCT person_id) = 2
);