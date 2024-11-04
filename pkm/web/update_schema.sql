-- Drop the existing table if it exists
DROP TABLE IF EXISTS sub_daily_moods;

-- Create the table with the correct schema
CREATE TABLE sub_daily_moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    logged_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    mood INTEGER CHECK (mood BETWEEN 1 AND 10),
    energy INTEGER CHECK (energy BETWEEN 1 AND 10),
    notes TEXT
);

-- Create daily_entries table if it doesn't exist
CREATE TABLE IF NOT EXISTS daily_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
