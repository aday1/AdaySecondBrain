#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
import os
import json
import sqlite3
from datetime import datetime, timedelta
import sys
import argparse
import markdown
import logging
from time import strftime

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pkm_manager import PKMManager
from utils import format_timestamp

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, 
            template_folder='templates',  # Add template folder
            static_folder='static')       # Add static folder
app.debug = True

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

pkm = PKMManager()

# Initialize database
def init_db():
    conn = pkm.get_db_connection()
    cursor = conn.cursor()
    
    # Create work_logs table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            project TEXT,
            description TEXT,
            total_hours REAL
        )
    ''')
    
    # Create habits table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create habit_logs table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    ''')

    # Create alcohol_logs table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alcohol_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            drink_type TEXT NOT NULL,
            units REAL NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create drink_types table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drink_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create daily_logs table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create daily_metrics table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            mood_rating INTEGER CHECK (mood_rating BETWEEN 1 AND 10),
            energy_level INTEGER CHECK (energy_level BETWEEN 1 AND 10),
            sleep_hours REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# Load configuration
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'web_enabled': False, 'username': 'admin', 'password_hash': None}

config = load_config()
app.secret_key = config.get('secret_key', os.urandom(24))

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/api/daily-data/<date>')
@login_required
def get_daily_data(date):
    conn = pkm.get_db_connection()
    cursor = conn.cursor()
    
    # Get daily metrics
    cursor.execute('''
        SELECT date, mood_rating, energy_level
        FROM daily_metrics
        WHERE date = ?
    ''', (date,))
    
    metrics_data = cursor.fetchall()
    
    # Get sub-daily moods
    cursor.execute('''
        SELECT logged_at, mood, energy
        FROM sub_daily_moods
        WHERE date(logged_at) = ?
        ORDER BY logged_at
    ''', (date,))
    
    mood_data = cursor.fetchall()
    
    metrics = [
        {"name": "Productivity", "color": "#4CAF50"},
        {"name": "Focus", "color": "#2196F3"},
        {"name": "Energy", "color": "#FFC107"}
    ]
    
    formatted_data = []
    
    # Add daily metrics
    for row in metrics_data:
        date_str, mood, energy = row
        formatted_data.append({
            "timestamp": f"{date_str} 12:00:00",  # Noon for daily metrics
            "values": [mood, mood, energy]  # Using mood for both productivity and focus
        })
    
    # Add sub-daily moods
    for row in mood_data:
        timestamp, mood, energy = row
        formatted_data.append({
            "timestamp": timestamp,
            "values": [mood, mood, energy]  # Using mood for both productivity and focus
        })
    
    # Sort by timestamp
    formatted_data.sort(key=lambda x: x["timestamp"])
    
    conn.close()
    return jsonify({
        "metrics": metrics,
        "dataPoints": formatted_data
    })

@app.route('/api/work-hours/<timeframe>')
@login_required
def get_work_hours(timeframe):
    conn = pkm.get_db_connection()
    cursor = conn.cursor()
    
    # Calculate date range based on timeframe
    today = datetime.now().date()
    if timeframe == 'day':
        start_date = today
    elif timeframe == 'week':
        start_date = today - timedelta(days=7)
    elif timeframe == 'month':
        start_date = today - timedelta(days=30)
    else:  # year
        start_date = today - timedelta(days=365)
    
    # Get work distribution data for the specified timeframe
    cursor.execute('''
        SELECT project as category, SUM(total_hours) as hours
        FROM work_logs
        WHERE date >= ?
        GROUP BY project
    ''', (start_date.strftime('%Y-%m-%d'),))
    
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        # Return sample data if no data exists
        return jsonify({
            'categories': ['Development', 'Meetings', 'Planning', 'Research', 'Breaks'],
            'hours': [4.5, 2, 1, 1.5, 1] if timeframe == 'day' else
                    [20, 8, 4, 6, 2] if timeframe == 'week' else
                    [80, 32, 16, 24, 8] if timeframe == 'month' else
                    [960, 384, 192, 288, 96]  # year
        })
    
    categories = [row[0] for row in data]
    hours = [row[1] for row in data]
    
    return jsonify({
        'categories': categories,
        'hours': hours
    })

@app.route('/api/work-hours', methods=['POST'])
@login_required
def log_work_hours():
    data = request.get_json()
    conn = pkm.get_db_connection()
    cursor = conn.cursor()
    
    # Calculate end time based on start time and total hours
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=float(data['hours']))
    
    cursor.execute('''
        INSERT INTO work_logs (date, start_time, end_time, project, description, total_hours)
        VALUES (date('now'), ?, ?, ?, ?, ?)
    ''', (start_time.strftime('%Y-%m-%d %H:%M:%S'),
          end_time.strftime('%Y-%m-%d %H:%M:%S'),
          data['category'],
          f"Work logged for {data['category']}",
          data['hours']))
    
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@app.route('/metrics')
@login_required
def metrics():
    return render_template('metrics.html')

@app.route('/work')
@login_required
def work():
    return render_template('work.html')

@app.route('/habits', methods=['GET', 'POST'])
@login_required
def habits():
    conn = pkm.get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'delete_habit' in request.form:
            # Delete habit
            habit_name = request.form['delete_habit']
            cursor.execute('DELETE FROM habit_logs WHERE habit_id IN (SELECT id FROM habits WHERE name = ?)', (habit_name,))
            cursor.execute('DELETE FROM habits WHERE name = ?', (habit_name,))
            flash(f'Habit "{habit_name}" deleted successfully')
        else:
            # Add new habit or log existing one
            habit_name = request.form.get('new-habit') if request.form.get('habit') == 'new' else request.form.get('habit')
            notes = request.form.get('notes', '')

            # First ensure the habit exists
            cursor.execute('INSERT OR IGNORE INTO habits (name) VALUES (?)', (habit_name,))
            
            # Get the habit_id
            cursor.execute('SELECT id FROM habits WHERE name = ?', (habit_name,))
            habit_id = cursor.fetchone()[0]
            
            # Log the habit completion
            cursor.execute('INSERT INTO habit_logs (habit_id, notes) VALUES (?, ?)', (habit_id, notes))
            flash(f'Habit "{habit_name}" logged successfully')

        conn.commit()

    # Get habits with their weekly completion counts and recent notes
    cursor.execute('''
        WITH weekly_counts AS (
            SELECT h.name, COUNT(hl.id) as count, GROUP_CONCAT(hl.notes) as notes
            FROM habits h
            LEFT JOIN habit_logs hl ON h.id = hl.habit_id
            AND hl.completed_at >= datetime('now', '-7 days')
            GROUP BY h.name
        )
        SELECT name, count, notes
        FROM weekly_counts
        ORDER BY count DESC, name
    ''')
    
    habits_data = cursor.fetchall()
    conn.close()

    return render_template('habits.html', habits=habits_data)

@app.route('/alcohol', methods=['GET', 'POST'])
@login_required
def alcohol():
    conn = pkm.get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        drink_type = request.form.get('drink_type')
        units = float(request.form.get('units'))
        notes = request.form.get('notes', '')

        # Insert the drink type if it's new
        cursor.execute('INSERT OR IGNORE INTO drink_types (name) VALUES (?)', (drink_type,))
        
        # Log the alcohol consumption
        cursor.execute('''
            INSERT INTO alcohol_logs (drink_type, units, notes)
            VALUES (?, ?, ?)
        ''', (drink_type, units, notes))
        
        conn.commit()
        flash('Alcohol consumption logged successfully')

    # Get all drink types
    cursor.execute('SELECT name FROM drink_types ORDER BY name')
    drink_types = [row[0] for row in cursor.fetchall()]

    # Get recent alcohol logs
    cursor.execute('''
        SELECT id, date, drink_type, units, notes
        FROM alcohol_logs
        ORDER BY date DESC
        LIMIT 50
    ''')
    alcohol_logs = cursor.fetchall()

    # Calculate weekly total
    cursor.execute('''
        SELECT SUM(units)
        FROM alcohol_logs
        WHERE date >= datetime('now', '-7 days')
    ''')
    weekly_total = cursor.fetchone()[0] or 0

    conn.close()

    return render_template('alcohol.html', 
                         drink_types=drink_types,
                         alcohol_logs=alcohol_logs,
                         weekly_total=weekly_total)

@app.route('/update_alcohol_log', methods=['POST'])
@login_required
def update_alcohol_log():
    data = request.get_json()
    conn = pkm.get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert the drink type if it's new
        cursor.execute('INSERT OR IGNORE INTO drink_types (name) VALUES (?)', (data['drink_type'],))
        
        # Update the log
        cursor.execute('''
            UPDATE alcohol_logs
            SET drink_type = ?, units = ?, notes = ?
            WHERE id = ?
        ''', (data['drink_type'], data['units'], data['notes'], data['id']))
        
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/daily_logs', methods=['GET', 'POST'])
@login_required
def daily_logs():
    conn = pkm.get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        date = request.form.get('date')
        content = request.form.get('content')

        cursor.execute('''
            INSERT OR REPLACE INTO daily_logs (date, content, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (date, content))
        
        conn.commit()
        flash('Daily log saved successfully')

    # Get recent daily logs
    cursor.execute('''
        SELECT date, content, created_at, updated_at
        FROM daily_logs
        ORDER BY date DESC
        LIMIT 30
    ''')
    logs = cursor.fetchall()
    conn.close()

    # Get today's date for the default value
    today = datetime.now().strftime('%Y-%m-%d')

    return render_template('daily_logs.html', logs=logs, today=today)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        config = load_config()
        if not config['web_enabled']:
            flash('Web interface is disabled')
            return redirect(url_for('login'))
            
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == config['username'] and check_password_hash(config['password_hash'], password):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def start_server(host='0.0.0.0', port=None):
    config = load_config()
    if not config['web_enabled']:
        print("Web interface is disabled. Enable it in web/config.json")
        return
    
    if port is None:
        port = config.get('port', 5000)
    
    app.run(host=host, port=port, debug=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PKM Web Interface')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, help='Port to listen on')
    args = parser.parse_args()
    
    start_server(host=args.host, port=args.port)
