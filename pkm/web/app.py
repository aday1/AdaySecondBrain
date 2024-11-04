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

# Configure logging before creating the app
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)
app.debug = True  # Enable debug mode

# Configure Werkzeug logger
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.DEBUG)

# Add request logging
@app.before_request
def before_request():
    app.logger.debug(f'\nRequest: {request.method} {request.url}')
    app.logger.debug(f'Headers: {dict(request.headers)}')
    app.logger.debug(f'Body: {request.get_data().decode()}')

@app.after_request
def after_request(response):
    app.logger.debug(f'Response Status: {response.status}')
    app.logger.debug(f'Response Headers: {dict(response.headers)}')
    return response

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

pkm = PKMManager()
app.logger.info(f"Database path: {pkm.db_path}")  # Debug output
app.logger.info(f"Database exists: {os.path.exists(pkm.db_path)}")  # Debug output

# Initialize database with sub_daily_moods table
def init_db():
    app.logger.info("Initializing database...")  # Debug output
    conn = pkm.get_db_connection()
    cursor = conn.cursor()
    
    # Create sub_daily_moods table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sub_daily_moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            logged_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            mood INTEGER,
            energy INTEGER,
            notes TEXT
        )
    ''')
    
    # Debug output - list all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    app.logger.info(f"Tables in database: {[table[0] for table in tables]}")  # Debug output
    
    conn.commit()
    conn.close()

# Call init_db when the app starts
init_db()

# Load configuration
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'web_enabled': False, 'username': 'admin', 'password_hash': None}

# Initialize app configuration from config.json
config = load_config()
app.secret_key = config.get('secret_key', os.urandom(24))

# Make config and global functions available to all templates
@app.context_processor
def inject_config():
    return dict(
        site_title=config.get('title', 'Personal Knowledge Management'),
        min=min  # Add min() function to templates
    )

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.template_filter('format_date')
def format_date_filter(date):
    """Convert date to format with month name"""
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%B %d, %Y')  # e.g., "January 01, 2024"

def get_mood_emoji(value):
    """Helper function to get mood emoji based on value"""
    if value <= 3:
        return '😫'
    elif value <= 5:
        return '😐'
    elif value <= 7:
        return '🙂'
    else:
        return '😊'

def get_energy_emoji(value):
    """Helper function to get energy emoji based on value"""
    if value <= 3:
        return '🔋'
    elif value <= 7:
        return '⚡'
    else:
        return '⚡⚡'

@app.route('/')
@login_required
def index():
    app.logger.info("Accessing index route...")  # Debug output
    conn = pkm.get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get unique projects
        app.logger.info("Fetching projects...")  # Debug output
        cursor.execute('SELECT DISTINCT project FROM work_logs WHERE project IS NOT NULL ORDER BY project')
        projects = [row[0] for row in cursor.fetchall()]
        app.logger.info(f"Found projects: {projects}")  # Debug output
        
        # Get unique habits
        app.logger.info("Fetching habits...")  # Debug output
        cursor.execute('SELECT name FROM habits ORDER BY name')
        habits = [row[0] for row in cursor.fetchall()]
        app.logger.info(f"Found habits: {habits}")  # Debug output
        
        # Get unique drink types
        app.logger.info("Fetching drink types...")  # Debug output
        cursor.execute('''
            SELECT DISTINCT drink_type 
            FROM alcohol_logs 
            WHERE drink_type IS NOT NULL 
            ORDER BY drink_type
        ''')
        drink_types = [row[0] for row in cursor.fetchall()]
        app.logger.info(f"Found drink types: {drink_types}")  # Debug output
        
        # Get today's sub-daily mood logs
        app.logger.info("Fetching today's mood logs...")  # Debug output
        cursor.execute('''
            SELECT logged_at, mood, energy, notes 
            FROM sub_daily_moods 
            WHERE date(logged_at) = date('now')
            ORDER BY logged_at DESC
        ''')
        sub_daily_logs = []
        for row in cursor.fetchall():
            timestamp, mood, energy, notes = row
            time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
            sub_daily_logs.append({
                'time': time,
                'mood': mood,
                'mood_emoji': get_mood_emoji(mood),
                'energy': energy,
                'energy_emoji': get_energy_emoji(energy),
                'notes': notes
            })
        app.logger.info(f"Found {len(sub_daily_logs)} mood logs for today")  # Debug output
        
        conn.close()
        
        return render_template('index.html', 
                             projects=projects, 
                             habits=habits, 
                             drink_types=drink_types,
                             sub_daily_logs=sub_daily_logs)
    except Exception as e:
        app.logger.error(f"Error in index route: {str(e)}")  # Debug output
        conn.close()
        raise

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

@app.route('/sub_daily_mood', methods=['POST'])
@login_required
def sub_daily_mood():
    try:
        mood = int(request.form.get('sub_mood'))
        energy = int(request.form.get('sub_energy'))
        notes = request.form.get('sub_notes')
        
        conn = pkm.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sub_daily_moods (mood, energy, notes)
            VALUES (?, ?, ?)
        ''', (mood, energy, notes))
        
        conn.commit()
        conn.close()
        
        flash('Mood state logged successfully')
    except ValueError:
        flash('Invalid input')
    except Exception as e:
        flash(f'Error: {str(e)}')
    
    return redirect(url_for('index'))

@app.route('/metrics', methods=['GET', 'POST'])
@login_required
def metrics():
    if request.method == 'POST':
        try:
            mood = int(request.form.get('mood'))
            energy = int(request.form.get('energy'))
            sleep = float(request.form.get('sleep'))
            notes = request.form.get('notes')
            
            pkm.log_daily_metrics(mood, energy, sleep, notes)
            flash('Metrics logged successfully')
        except ValueError:
            flash('Invalid input')
        return redirect(url_for('metrics'))
        
    # Get today's metrics
    conn = pkm.get_db_connection()
    cursor = conn.cursor()
    
    # Get today's metrics
    cursor.execute('SELECT * FROM daily_metrics WHERE date = date("now")')
    today_metrics = cursor.fetchone()
    
    # Get historical metrics for the past 30 days
    cursor.execute('''
        SELECT date, mood_rating, energy_level, sleep_hours, notes 
        FROM daily_metrics 
        WHERE date >= date('now', '-30 days')
        ORDER BY date ASC
    ''')
    historical_metrics = cursor.fetchall()
    
    # Format historical metrics for Chart.js
    dates = []
    moods = []
    energies = []
    sleep_hours = []
    
    for metric in historical_metrics:
        dates.append(metric[0])  # date
        moods.append(metric[1])  # mood_rating
        energies.append(metric[2])  # energy_level
        sleep_hours.append(metric[3])  # sleep_hours
    
    conn.close()
    
    return render_template('metrics.html', 
                         metrics=today_metrics,
                         dates=dates,
                         moods=moods,
                         energies=energies,
                         sleep_hours=sleep_hours)

@app.route('/work', methods=['GET', 'POST'])
@login_required
def work():
    if request.method == 'POST':
        try:
            project = request.form.get('project')
            if project == 'new':
                project = request.form.get('new-project')
            description = request.form.get('description')
            hours = float(request.form.get('hours'))
            
            pkm.log_work_hours_direct(hours, project=project, description=description)
            flash('Work logged successfully')
        except ValueError:
            flash('Invalid input: Please enter a valid number of hours')
        except Exception as e:
            flash(f'Error: {str(e)}')
        return redirect(url_for('work'))
        
    # Get recent work logs and unique projects
    conn = pkm.get_db_connection()
    cursor = conn.cursor()
    
    # Get work logs with ID included
    cursor.execute('''
        SELECT date, project, description, total_hours, id
        FROM work_logs 
        WHERE date >= date('now', '-7 days')
        ORDER BY date DESC
    ''')
    work_logs = cursor.fetchall()
    
    # Get unique projects
    cursor.execute('SELECT DISTINCT project FROM work_logs WHERE project IS NOT NULL ORDER BY project')
    projects = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('work.html', work_logs=work_logs, projects=projects)

@app.route('/update_work_log', methods=['POST'])
@login_required
def update_work_log():
    try:
        data = request.get_json()
        log_id = data.get('id')
        project = data.get('project')
        description = data.get('description')
        total_hours = float(data.get('total_hours'))
        
        conn = pkm.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE work_logs 
            SET project = ?, description = ?, total_hours = ?
            WHERE id = ?
        ''', (project, description, total_hours, log_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/delete_project', methods=['POST'])
@login_required
def delete_project():
    try:
        data = request.get_json()
        project_name = data.get('project')
        
        if not project_name:
            return jsonify({'status': 'error', 'message': 'Project name is required'}), 400
            
        conn = pkm.get_db_connection()
        cursor = conn.cursor()
        
        # Delete all work logs for this project
        cursor.execute('DELETE FROM work_logs WHERE project = ?', (project_name,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/delete_habit', methods=['POST'])
@login_required
def delete_habit():
    try:
        data = request.get_json()
        habit_name = data.get('habit')
        
        if not habit_name:
            return jsonify({'status': 'error', 'message': 'Habit name is required'}), 400
            
        conn = pkm.get_db_connection()
        cursor = conn.cursor()
        
        # First get the habit ID
        cursor.execute('SELECT id FROM habits WHERE name = ?', (habit_name,))
        habit = cursor.fetchone()
        
        if habit:
            habit_id = habit[0]
            # Delete all habit logs for this habit
            cursor.execute('DELETE FROM habit_logs WHERE habit_id = ?', (habit_id,))
            # Delete the habit itself
            cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
            
            conn.commit()
            conn.close()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Habit not found'}), 404
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/habits', methods=['GET', 'POST'])
@login_required
def habits():
    if request.method == 'POST':
        try:
            habit = request.form.get('habit')
            notes = request.form.get('notes')
            
            pkm.log_habit(habit, notes=notes)
            flash('Habit logged successfully')
        except Exception as e:
            flash(f'Error: {str(e)}')
        return redirect(url_for('habits'))
        
    # Get habits, their completion counts, and recent notes
    conn = pkm.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            h.name,
            COUNT(DISTINCT hl1.id) as completions,
            GROUP_CONCAT(DISTINCT hl2.notes) as recent_notes
        FROM habits h
        LEFT JOIN habit_logs hl1 
            ON h.id = hl1.habit_id
            AND hl1.completed_at >= date('now', '-7 days')
        LEFT JOIN (
            SELECT habit_id, notes
            FROM habit_logs
            WHERE notes IS NOT NULL AND notes != ''
            AND completed_at >= date('now', '-7 days')
            ORDER BY completed_at DESC
        ) hl2 ON h.id = hl2.habit_id
        GROUP BY h.name
    ''')
    habits = cursor.fetchall()
    conn.close()
    
    return render_template('habits.html', habits=habits)

@app.route('/alcohol', methods=['GET', 'POST'])
@login_required
def alcohol():
    try:
        if request.method == 'POST':
            try:
                drink_type = request.form.get('drink_type')
                if not drink_type:
                    raise ValueError("Drink type is required")
                
                units = request.form.get('units')
                if not units:
                    raise ValueError("Units are required")
                units = float(units)
                if units <= 0:
                    raise ValueError("Units must be greater than 0")
                
                notes = request.form.get('notes')
                
                pkm.log_alcohol(drink_type, units, notes)
                flash('Alcohol consumption logged successfully')
            except ValueError as e:
                flash(f'Invalid input: {str(e)}')
            except Exception as e:
                flash(f'Error logging alcohol consumption: {str(e)}')
            return redirect(url_for('alcohol'))
            
        # Get recent alcohol logs and unique drink types
        conn = pkm.get_db_connection()
        cursor = conn.cursor()
        
        # Get recent logs with IDs and calculate weekly total
        cursor.execute('''
            SELECT id, date, drink_type, units, notes,
                   (SELECT SUM(units) 
                    FROM alcohol_logs 
                    WHERE date >= date('now', '-7 days')) as weekly_total
            FROM alcohol_logs
            WHERE date >= date('now', '-7 days')
            ORDER BY date DESC
        ''')
        alcohol_logs = cursor.fetchall()
        
        # Get unique drink types
        cursor.execute('''
            SELECT DISTINCT drink_type 
            FROM alcohol_logs 
            WHERE drink_type IS NOT NULL 
            ORDER BY drink_type
        ''')
        drink_types = [row[0] for row in cursor.fetchall()]
        
        # Calculate weekly total
        weekly_total = alcohol_logs[0][5] if alcohol_logs else 0
        
        conn.close()
        
        return render_template('alcohol.html', 
                             alcohol_logs=alcohol_logs, 
                             drink_types=drink_types,
                             weekly_total=weekly_total)
    except Exception as e:
        flash(f'An unexpected error occurred: {str(e)}')
        return redirect(url_for('index'))

@app.route('/update_alcohol_log', methods=['POST'])
@login_required
def update_alcohol_log():
    try:
        data = request.get_json()
        log_id = data.get('id')
        drink_type = data.get('drink_type')
        units = float(data.get('units'))
        notes = data.get('notes')
        
        conn = pkm.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alcohol_logs 
            SET drink_type = ?, units = ?, notes = ?
            WHERE id = ?
        ''', (drink_type, units, notes, log_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/daily_logs', methods=['GET', 'POST'])
@login_required
def daily_logs():
    if request.method == 'POST':
        try:
            # Create today's log
            today = datetime.now().strftime('%Y-%m-%d')
            file_path = os.path.join(pkm.daily_dir, f'{today}.md')
            
            # Check if file already exists
            if os.path.exists(file_path):
                flash('Today\'s log already exists')
                return redirect(url_for('daily_logs'))
            
            # Create daily directory if it doesn't exist
            os.makedirs(pkm.daily_dir, exist_ok=True)
            
            # Get template content
            template_path = os.path.join(pkm.templates_dir, 'daily_template.md')
            try:
                with open(template_path, 'r') as f:
                    template_content = f.read()
            except FileNotFoundError:
                template_content = f"# Daily Log - {today}\n\n## Notes\n\n## Tasks\n\n## Reflections\n"
            
            # Create the new log file
            with open(file_path, 'w') as f:
                f.write(template_content)
            
            flash('Today\'s log created successfully')
            return redirect(url_for('edit_log', date=today))
        except Exception as e:
            flash(f'Error creating log: {str(e)}')
            return redirect(url_for('daily_logs'))
    
    logs = []
    
    try:
        if os.path.exists(pkm.daily_dir):
            for log_file in sorted(os.listdir(pkm.daily_dir), reverse=True)[:5]:
                if log_file.endswith('.md'):
                    with open(os.path.join(pkm.daily_dir, log_file), 'r') as f:
                        content = f.read()
                        html_content = markdown.markdown(content, extensions=['fenced_code', 'tables'])
                        logs.append({
                            'date': log_file.replace('.md', ''),
                            'content': html_content,
                            'raw_content': content
                        })
    except Exception as e:
        flash(f'Error reading logs: {str(e)}')
    
    return render_template('daily_logs.html', logs=logs)

@app.route('/edit_log/<date>', methods=['GET', 'POST'])
@login_required
def edit_log(date):
    file_path = os.path.join(pkm.daily_dir, f'{date}.md')
    
    if request.method == 'POST':
        content = request.form.get('content')
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            flash('Log updated successfully')
            return redirect(url_for('daily_logs'))
        except Exception as e:
            flash(f'Error updating log: {str(e)}')
            return redirect(url_for('daily_logs'))
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return render_template('edit_log.html', date=date, content=content)
    except FileNotFoundError:
        flash('Log file not found')
        return redirect(url_for('daily_logs'))

# Error handlers
@app.errorhandler(405)
def method_not_allowed(e):
    flash('Invalid request method')
    return redirect(url_for('daily_logs'))

@app.errorhandler(500)
def internal_server_error(e):
    flash('An internal server error occurred. Please try again later.')
    return redirect(url_for('index'))

def start_server(host='0.0.0.0', port=None):
    config = load_config()
    if not config['web_enabled']:
        print("Web interface is disabled. Enable it in web/config.json")
        return
    
    # Use port from config if not specified
    if port is None:
        port = config.get('port', 5000)
    
    app.run(host=host, port=port, debug=True)  # Enable debug mode

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PKM Web Interface')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, help='Port to listen on')
    args = parser.parse_args()
    
    start_server(host=args.host, port=args.port)
