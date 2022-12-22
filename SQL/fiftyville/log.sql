-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Get crime report at given day and on given street:
SELECT description FROM crime_scene_reports
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND street LIKE 'Humphrey Street';

-- Get names and transcrips of witnesses from the 'interviews' table:
SELECT name, transcript FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day = 28;

-- Check to see if there are multiple 'Eugenes':
SELECT name FROM people
 WHERE name LIKE 'Eugene';
-- Only one 'Eugene' exists per the output.

-- Get transcripts of each witness that mentions the bakery:
SELECT name, transcript FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND transcript LIKE '%bakery%'
ORDER BY name;
-- Witnesses include: Eugene, Raymond, and Ruth.

-- Check first clue from Eugene by getting all Legget Street ATM withdrawals and their corresponding account numbers
SELECT account_number, amount
  FROM atm_transactions
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND atm_location LIKE '%Leggett Street%'
   AND transaction_type LIKE '%withdraw%'
ORDER BY amount;

-- Get name associated with each account number
SELECT name, atm_transactions.amount FROM people
  JOIN bank_accounts
    ON people.id = bank_accounts.person_id
  JOIN atm_transactions
    ON bank_accounts.account_number = atm_transactions.account_number
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND atm_transactions.year = 2021
   AND atm_transactions.month = 7
   AND atm_transactions.day = 28
   AND atm_transactions.atm_location LIKE '%Leggett Street%'
   AND atm_transactions.transaction_type LIKE '%withdraw%'
ORDER BY amount;

-- Get details of Fiftyville airport (departure)
SELECT abbreviation, full_name, city
  FROM airports
 WHERE city = 'Fiftyville';

-- Check second clue from Raymond by getting the < 60 second phone call.
-- Get the flights on July 29 from Fiftyville airport, and order by time.
SELECT flights.id, full_name, city, flights.hour, flights.minute
  FROM airports
  JOIN flights
    ON airports.id = flights.destination_airport_id
 WHERE flights.origin_airport_id = (
SELECT id
  FROM airports
 WHERE city LIKE '%Fiftyville%')
   AND flights.year = 2021
   AND flights.month = 7
   AND flights.day = 29
ORDER BY flights.hour, flights.minute;
-- Result shows flight id #36 at 8:20AM (earliest) to LaGuardia Airport in New York City.

-- Check list of passengers on flight #36. Order names by passport number.
SELECT passengers.flight_id, name, passengers.passport_number, passengers.seat
  FROM people
  JOIN passengers
    ON people.passport_number = passengers.passport_number
  JOIN flights
    ON passengers.flight_id = flights.id
 WHERE flights.year = 2021
   AND flights.month = 7
   AND flights.day = 29
   AND flights.hour = 8
   AND flights.minute = 20
   ORDER BY passengers.passport_number;

-- Check third clue from Ruth by getting the time the thief left the bakery.
SELECT name, bakery_security_logs.hour, bakery_security_logs.minute
  FROM people
  JOIN bakery_security_logs
-- Check license plates of cars within that time frame. Then, check the names of the vehicles owners.
    ON people.license_plate = bakery_security_logs.license_plate
 WHERE bakery_security_logs.year = 2021
   AND bakery_security_logs.month = 7
   AND bakery_security_logs.day = 28
   AND bakery_security_logs.activity LIKE '%exit%'
   AND bakery_security_logs.hour = 10
   AND bakery_security_logs.minute >= 15
   AND bakery_security_logs.minute <= 25
   ORDER BY bakery_security_logs.minute;

-- Get Bruce's phone number since they are the thief.
SELECT phone_number
  FROM people
 WHERE name = 'Bruce';
-- Bruce's phone number: (367) 555-5533

-- Get accomplice that receievd Bruce's phone call
SELECT name
  FROM people
 WHERE phone_number = (
SELECT receiver
  FROM phone_calls
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND duration < 60
   AND caller = '(367) 555-5533');