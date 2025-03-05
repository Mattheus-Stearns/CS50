-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Using information from the problem set
SELECT *
FROM crime_scene_reports
LIMIT 10;

SELECT *
FROM crime_scene_reports
WHERE street = 'Humphrey Street'
AND year = 2024
AND month = 7
AND day = 28;
-- Theft at 10:15am, check interviews

SELECT *
FROM interviews
WHERE id < 164
AND id > 160;
-- Thief left within 10 minutes of the theft
-- Earlier that morning at the atm on Leggett Street the thief withdrew money
-- As the thief left the bakery, they had less than a one minute long call planning their escape flight on the earliest flight the next morning

-- List of suspects 
SELECT name
FROM people
WHERE license_plate IN (
    SELECT DISTINCT license_plate
    FROM bakery_security_logs
    WHERE hour <= 10
    AND minute <= 25
    AND minute >= 15
    AND year = 2024
    AND month = 7
    AND day = 28
) AND id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE atm_location = 'Leggett Street'
        AND year = 2024
        AND month = 7
        AND day = 28
        AND transaction_type = 'withdraw'
    )
);
-- Four Suspects: Iman, Luca, Diana, and Bruce

-- Check phone calls of suspects
SELECT name
FROM people
WHERE phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE caller IN (
        SELECT phone_number
        FROM people
        WHERE name = 'Iman'
        OR name = 'Luca'
        OR name = 'Diana'
        OR name = 'Bruce'
    )AND year = 2024
    AND month = 7
    AND day = 28
    AND duration < 60
); -- Only Diana and Bruce made calls during that time frame

-- Check the airport flights
SELECT name
FROM people
WHERE passport_number IN (
    SELECT passport_number
    FROM passengers
    WHERE flight_id = (
        SELECT id
        FROM flights
        WHERE id IN (
            SELECT flight_id
            FROM passengers
            WHERE passport_number IN (
                SELECT passport_number
                FROM people
                WHERE name = 'Diana'
                OR name = 'Bruce'
            )
        ) AND day = 29
        AND month = 7
        AND year = 2024
        ORDER BY hour ASC
        LIMIT 1
    )
) AND (
    name = 'Diana'
    OR name = 'Bruce'
);
-- Bruce is the culprit

-- Find the city bruce escaped to
SELECT city
FROM airports
WHERE id = (
    SELECT destination_airport_id
    FROM flights
    WHERE id = (
        SELECT flight_id
        FROM passengers
        WHERE passport_number = (
            SELECT passport_number
            FROM people
            WHERE name = 'Bruce'
        )
    )
);
-- It's New York City

-- The accomplice can be gotten through Bruce's phone logs
SELECT name
FROM people
WHERE phone_number IN (
    SELECT receiver
    FROM phone_calls
    WHERE caller IN (
        SELECT phone_number
        FROM people
        WHERE name = 'Bruce'
    )AND year = 2024
    AND month = 7
    AND day = 28
    AND duration < 60
);
-- Therefore the accomplice is Robin
