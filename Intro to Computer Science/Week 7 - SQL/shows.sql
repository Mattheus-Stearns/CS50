SELECT show_id 
FROM ratings 
WHERE rating >= 9.0 AND votes >= 100 
LIMIT 10;

SELECT title 
FROM shows 
WHERE id IN (
    SELECT show_id 
    FROM ratings 
    WHERE rating >= 9.0 AND votes >= 100
) LIMIT 10; 

-- One to One Relationship
SELECT title, rating, votes
FROM shows
JOIN ratings ON shows.id = ratings.show_id
WHERE rating >= 9.0 AND votes >= 100
LIMIT 10;

SELECT genre 
FROM genres 
WHERE show_id = (
    SELECT id 
    FROM shows 
    WHERE title = 'Catweazle'
);

-- One to Many relationship
SELECT title, genre
FROM shows
JOIN genres ON shows.id = genres.show_id
WHERE id = (
    SELECT id 
    FROM shows 
    WHERE title = 'Catweazle'
);


SELECT name 
FROM people 
WHERE id IN (
    SELECT person_id 
    FROM stars 
    WHERE show_id = (
        SELECT id 
        FROM shows 
        WHERE title = 'The Office' AND year = 2005
    )
);

-- Many to Many relationship

-- Faster
SELECT title
FROM shows
WHERE id IN (
    SELECT show_id
    FROM stars
    WHERE person_id = (
        SELECT id
        FROM people
        WHERE name = 'Steve Carell'
    )
);

-- It's B-Tree:
CREATE INDEX name_index ON people (name);
CREATE INDEX person_index ON stars (person_id);

-- Slower
SELECT title
FROM shows
JOIN stars ON shows.id = stars.show_id
JOIN people ON stars.person_id = people.id
WHERE name = 'Steve Carell';

-- Slower
SELECT title
FROM shows, stars, people
WHERE shows.id = stars.show_id 
AND people.id = stars.person_id
AND name = 'Steve Carell';