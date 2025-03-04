-- Create the table if it does not exist
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL,
    problem TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert data into the table
INSERT INTO favorites (language, problem) VALUES ('SQL', 'Fiftyville');

-- Select the most popular language
SELECT language, COUNT(*) FROM favorites GROUP BY language ORDER BY COUNT(*) DESC LIMIT 1;

-- Select entries where timestamp is NULL
SELECT * FROM favorites WHERE timestamp IS NULL;

DELETE FROM favorites WHERE timestamp IS NULL;

SELECT * FROM favorites;

UPDATE favorites
SET language = 'SQL', problem = 'Fiftyville';

SELECT *
FROM favorites;