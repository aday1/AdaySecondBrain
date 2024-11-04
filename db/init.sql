-- Core tables for personal metrics tracking

-- Habits tracking
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    frequency TEXT NOT NULL, -- daily, weekly, monthly
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Habit logs for tracking completion
CREATE TABLE IF NOT EXISTS habit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (habit_id) REFERENCES habits(id)
);

-- Alcohol consumption tracking
CREATE TABLE IF NOT EXISTS alcohol_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    drink_type TEXT NOT NULL,
    units FLOAT NOT NULL,
    notes TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Work hours tracking
CREATE TABLE IF NOT EXISTS work_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    project TEXT,
    description TEXT,
    total_hours FLOAT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Daily metrics for general tracking
CREATE TABLE IF NOT EXISTS daily_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    mood_rating INTEGER CHECK (mood_rating BETWEEN 1 AND 10),
    energy_level INTEGER CHECK (energy_level BETWEEN 1 AND 10),
    sleep_hours FLOAT,
    notes TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sub-daily mood tracking for more granular metrics
CREATE TABLE IF NOT EXISTS sub_daily_moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood INTEGER CHECK (mood BETWEEN 1 AND 10),
    energy INTEGER CHECK (energy BETWEEN 1 AND 10),
    notes TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Goals and plans
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    target_date DATE,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Daily entries for comprehensive daily logging
CREATE TABLE IF NOT EXISTS daily_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
