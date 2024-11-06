from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta
import random

app = Flask(__name__)

@app.route('/api/daily-data/<date>')
def get_daily_data(date):
    data = query_daily_data(date)
    return jsonify(data)

@app.route('/api/work-hours/<timeframe>')
def get_work_hours(timeframe):
    data = query_work_hours(timeframe)
    return jsonify(data)

def query_daily_data(date):
    # Generate sample data for demonstration
    # In production, this would query your database
    metrics = [
        {"name": "Productivity", "color": "#4CAF50"},
        {"name": "Focus", "color": "#2196F3"},
        {"name": "Energy", "color": "#FFC107"}
    ]
    
    # Generate 24 hours of data points
    base_date = datetime.strptime(date, '%Y-%m-%d')
    data_points = []
    
    for hour in range(24):
        for minute in range(0, 60, 15):  # Data points every 15 minutes
            timestamp = base_date + timedelta(hours=hour, minutes=minute)
            values = [random.uniform(0, 100) for _ in metrics]
            data_points.append({
                "timestamp": timestamp.isoformat(),
                "values": values
            })
    
    return {
        "metrics": metrics,
        "dataPoints": data_points
    }

def query_work_hours(timeframe):
    # In production, this would query your database
    # Generate sample data based on timeframe
    categories = ['Development', 'Meetings', 'Planning', 'Research', 'Breaks']
    
    if timeframe == 'day':
        hours = [4.5, 2, 1, 1.5, 1]
    elif timeframe == 'week':
        hours = [20, 8, 4, 6, 2]
    elif timeframe == 'month':
        hours = [80, 32, 16, 24, 8]
    else:  # year
        hours = [960, 384, 192, 288, 96]
    
    return {
        'categories': categories,
        'hours': hours
    }

@app.route('/')
def dashboard():
    # Get today's metrics for the dashboard
    today = datetime.now().strftime('%Y-%m-%d')
    daily_data = query_daily_data(today)
    work_data = query_work_hours('day')
    
    # Get the latest metrics values
    latest_metrics = None
    if daily_data['dataPoints']:
        latest_point = daily_data['dataPoints'][-1]
        latest_metrics = {
            'productivity': round(latest_point['values'][0]),
            'focus': round(latest_point['values'][1]),
            'energy': round(latest_point['values'][2])
        }
    
    return render_template('dashboard.html', 
                         metrics=latest_metrics,
                         work_data=work_data)

@app.route('/metrics')
def metrics():
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('metrics.html', today=today)

@app.route('/daily')
def daily_overview():
    return render_template('daily_overview.html')

if __name__ == '__main__':
    app.run(debug=True)
