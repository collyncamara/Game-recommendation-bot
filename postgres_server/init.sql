-- Creates a blank table for storing games and their selection counts.
CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    times_selected INT DEFAULT 0
);