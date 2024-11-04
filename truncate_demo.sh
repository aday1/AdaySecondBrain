#!/bin/bash

set -e

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to validate date format
validate_date() {
    if ! date -d "$1" >/dev/null 2>&1; then
        echo -e "${RED}Invalid date format. Please use YYYY-MM-DD format.${NC}"
        return 1
    fi
    return 0
}

# Set the path to the virtual environment's Python
VENV_PYTHON="pkm_venv/bin/python"

# Check if the virtual environment's Python exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${RED}Error: Virtual environment Python not found at $VENV_PYTHON${NC}"
    echo "Please ensure the virtual environment is set up correctly."
    exit 1
fi

# Create a temporary Python script to get and truncate date range
cat > truncate_demo_data.py << 'EOF'
import json
from datetime import datetime
import sys
from pkm.generate_demo_data import DemoDataGenerator

def get_date_range(data):
    dates = []
    
    # Collect dates from all relevant sections
    if 'daily_entries' in data:
        dates.extend(entry['date'] for entry in data['daily_entries'])
    
    if 'sub_daily_moods' in data:
        dates.extend(mood['logged_at'].split()[0] for mood in data['sub_daily_moods'])
    
    if 'daily_metrics' in data:
        dates.extend(metric['date'] for metric in data['daily_metrics'])
    
    if 'work_logs' in data:
        dates.extend(log['date'] for log in data['work_logs'])
    
    if 'habit_logs' in data:
        dates.extend(log['completed_at'].split()[0] for log in data['habit_logs'])
    
    if not dates:
        return None, None
        
    return min(dates), max(dates)

def truncate_data(data, start_date, end_date):
    # Convert to datetime objects for comparison
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Truncate daily entries
    if 'daily_entries' in data:
        data['daily_entries'] = [
            entry for entry in data['daily_entries']
            if start_date <= entry['date'] <= end_date
        ]
    
    # Truncate sub daily moods
    if 'sub_daily_moods' in data:
        data['sub_daily_moods'] = [
            mood for mood in data['sub_daily_moods']
            if start_date <= mood['logged_at'].split()[0] <= end_date
        ]
    
    # Truncate daily metrics
    if 'daily_metrics' in data:
        data['daily_metrics'] = [
            metric for metric in data['daily_metrics']
            if start_date <= metric['date'] <= end_date
        ]
    
    # Truncate work logs
    if 'work_logs' in data:
        data['work_logs'] = [
            log for log in data['work_logs']
            if start_date <= log['date'] <= end_date
        ]
    
    # Truncate habit logs
    if 'habit_logs' in data:
        data['habit_logs'] = [
            log for log in data['habit_logs']
            if start_date <= log['completed_at'].split()[0] <= end_date
        ]
    
    # Truncate alcohol logs
    if 'alcohol_logs' in data:
        data['alcohol_logs'] = [
            log for log in data['alcohol_logs']
            if start_date <= log['date'] <= end_date
        ]
    
    return data

# Main execution
try:
    with open('demo_data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("no_file")
    sys.exit(1)
except json.JSONDecodeError:
    print("invalid_json")
    sys.exit(1)

if len(sys.argv) == 1:
    # Just get date range
    min_date, max_date = get_date_range(data)
    if min_date and max_date:
        print(f"{min_date},{max_date}")
    else:
        print("no_data")
else:
    # Truncate data
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    truncated_data = truncate_data(data, start_date, end_date)
    
    # Save truncated data back to demo_data.json
    with open('demo_data.json', 'w') as f:
        json.dump(truncated_data, f, indent=2)
    
    # Import truncated data into database
    generator = DemoDataGenerator()
    generator.import_to_database(truncated_data)
    print("success")
EOF

# Get date range from demo_data.json
echo -e "${YELLOW}Checking available date range in demo_data.json...${NC}"
date_range=$("$VENV_PYTHON" truncate_demo_data.py)

case $date_range in
    "no_file")
        echo -e "${RED}Error: demo_data.json not found${NC}"
        rm truncate_demo_data.py
        exit 1
        ;;
    "invalid_json")
        echo -e "${RED}Error: demo_data.json is not valid JSON${NC}"
        rm truncate_demo_data.py
        exit 1
        ;;
    "no_data")
        echo -e "${RED}Error: No date data found in demo_data.json${NC}"
        rm truncate_demo_data.py
        exit 1
        ;;
    *)
        IFS=',' read -r min_date max_date <<< "$date_range"
        echo -e "${GREEN}Available date range: ${YELLOW}$min_date${NC} to ${YELLOW}$max_date${NC}"
        ;;
esac

# Ask for start and end dates
while true; do
    read -p "Enter start date (YYYY-MM-DD): " start_date
    if ! validate_date "$start_date"; then
        continue
    fi
    if [[ "$start_date" < "$min_date" ]]; then
        echo -e "${RED}Start date must be on or after $min_date${NC}"
        continue
    fi
    break
done

while true; do
    read -p "Enter end date (YYYY-MM-DD): " end_date
    if ! validate_date "$end_date"; then
        continue
    fi
    if [[ "$end_date" < "$start_date" ]]; then
        echo -e "${RED}End date must be after start date${NC}"
        continue
    fi
    if [[ "$end_date" > "$max_date" ]]; then
        echo -e "${RED}End date must be on or before $max_date${NC}"
        continue
    fi
    break
done

echo -e "${YELLOW}Truncating demo data and updating database...${NC}"
result=$("$VENV_PYTHON" truncate_demo_data.py "$start_date" "$end_date")

if [ "$result" = "success" ]; then
    echo -e "${GREEN}Successfully truncated demo_data.json and updated database for date range: ${YELLOW}$start_date${NC} to ${YELLOW}$end_date${NC}"
else
    echo -e "${RED}Error: Failed to truncate demo data${NC}"
    exit 1
fi

# Clean up
rm truncate_demo_data.py
