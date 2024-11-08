#!/bin/bash

# Color definitions
RED='\033[0;31m'
NC='\033[0m' # No Color

# Emoji definitions
EMOJI_ERROR="❌"
EMOJI_SUCCESS="✅"
EMOJI_BACKUP="💾"
EMOJI_RESTORE="🔄"
EMOJI_CONFIG="⚙️"
EMOJI_WEB="🌐"
EMOJI_DB="🗄️"
EMOJI_DAILY="📅"
EMOJI_HELP="❓"

# Check for gum installation
check_gum() {
    if ! command -v gum &> /dev/null; then
        echo "Installing gum for modern terminal UI..."
        if command -v brew &> /dev/null; then
            brew install gum
        elif command -v apt-get &> /dev/null; then
            sudo mkdir -p /etc/apt/keyrings
            curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
            echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list
            sudo apt update && sudo apt install gum
        else
            echo "Please install gum manually: https://github.com/charmbracelet/gum#installation"
            exit 1
        fi
    fi
}

# Function to display styled error
display_error() {
    local error_msg="$1"
    gum style --border="rounded" --border-foreground="red" --foreground="red" "$EMOJI_ERROR $error_msg"
}

# Function to display styled success
display_success() {
    local msg="$1"
    gum style --border="rounded" --border-foreground="green" --foreground="green" "$EMOJI_SUCCESS $msg"
}

# Function to wait for user input
wait_for_key() {
    gum input --placeholder="Press Enter to continue..."
}

# Check if virtual environment exists
if [ ! -d "pkm_venv" ]; then
    display_error "Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Activate virtual environment
VENV_ACTIVATE="pkm_venv/bin/activate"
if [ ! -f "$VENV_ACTIVATE" ]; then
    display_error "Virtual environment activation script not found. Please run install.sh first."
    exit 1
fi

source "$VENV_ACTIVATE"

# Database paths
DB_PATH="pkm/db/pkm.db"
INIT_SQL="db/init.sql"
BACKUP_DIR="pkm/db/backups"
LAST_BACKUP_FILE="pkm/db/.last_backup"

# MD files paths
DAILY_DIR="daily"
MD_BACKUP_DIR="pkm/db/md_backups"

# Function to show help
show_help() {
    gum style --border="rounded" --border-foreground="blue" "
    $EMOJI_HELP PKM System Launcher

    Usage: ./pkm.sh [option]

    Options:
    $EMOJI_WEB web           Start the web interface
    $EMOJI_CONFIG config        Open the configuration menu
    $EMOJI_DB init-db       Initialize the database
    $EMOJI_BACKUP backup-db     Create a database backup
    $EMOJI_RESTORE restore-db    Restore database from backup
    $EMOJI_BACKUP backup-md     Create a backup of markdown files
    $EMOJI_RESTORE restore-md    Restore markdown files from backup
    $EMOJI_HELP help          Show this help message

    No option will start the menu interface"
}

# Function to backup markdown files
backup_md() {
    mkdir -p "$MD_BACKUP_DIR"
    TIMESTAMP=$(get_formatted_timestamp)
    BACKUP_PATH="$MD_BACKUP_DIR/md_${TIMESTAMP}.tar.gz"
    
    if [ -d "$DAILY_DIR" ]; then
        gum spin --spinner dot --title "Creating markdown backup..." -- tar -czf "$BACKUP_PATH" "$DAILY_DIR"
        if [ $? -eq 0 ]; then
            display_success "Markdown files backed up to: $BACKUP_PATH"
            if [ "$1" != "silent" ]; then
                wait_for_key
            fi
        else
            display_error "Error creating markdown backup."
            wait_for_key
            exit 1
        fi
    else
        display_error "Daily directory not found."
        wait_for_key
        exit 1
    fi
}

# Function to restore markdown files
restore_md() {
    if [ ! -d "$MD_BACKUP_DIR" ]; then
        display_error "No markdown backups directory found."
        wait_for_key
        exit 1
    fi

    # List available backups with most recent first
    echo "Available markdown backups (most recent first):"
    BACKUPS=($(ls -1t "$MD_BACKUP_DIR"))
    SELECTED=$(gum choose "Cancel restore" "${BACKUPS[@]}")
    
    if [ "$SELECTED" = "Cancel restore" ]; then
        echo "Markdown restore cancelled."
        wait_for_key
        return
    fi
    
    # Confirm restore
    if gum confirm "Are you sure you want to restore markdown files from $SELECTED?"; then
        # Create a backup of current markdown files before restore
        echo "Creating backup of current markdown files before restore..."
        backup_md "silent"
        
        # Remove existing daily directory and restore from backup
        rm -rf "$DAILY_DIR"
        gum spin --spinner dot --title "Restoring from backup..." -- tar -xzf "$MD_BACKUP_DIR/$SELECTED"
        
        if [ $? -eq 0 ]; then
            display_success "Markdown files restored successfully from: $SELECTED"
            wait_for_key
        else
            display_error "Error restoring markdown files."
            wait_for_key
            exit 1
        fi
    else
        echo "Markdown restore cancelled."
        wait_for_key
    fi
}

# Function to initialize database
init_db() {
    gum style --border="rounded" "Database Initialization Information:" \
    "--------------------------------" \
    "This will create or reinitialize the following tables:" \
    "1. habits - Habit tracking definitions" \
    "2. habit_logs - Daily habit completion records" \
    "3. alcohol_logs - Alcohol consumption tracking" \
    "4. work_logs - Work hours and project tracking" \
    "5. daily_metrics - Daily mood, energy, and sleep tracking" \
    "6. goals - Goal tracking and planning"

    if [ -f "$DB_PATH" ]; then
        if gum confirm "Database already exists. Do you want to reinitialize it?"; then
            echo "Backing up existing database before reinitialization..."
            backup_db "silent"
            echo "Removing existing database..."
            rm "$DB_PATH"
        else
            echo "Database initialization cancelled."
            wait_for_key
            return
        fi
    fi

    # Ask about markdown files
    if [ -d "$DAILY_DIR" ] && [ "$(ls -A $DAILY_DIR)" ]; then
        if gum confirm "Do you want to backup and remove existing markdown files as well?"; then
            echo "Backing up markdown files before removal..."
            backup_md "silent"
            echo "Removing markdown files..."
            rm -rf "$DAILY_DIR"
            mkdir -p "$DAILY_DIR"
        fi
    fi
    
    gum spin --spinner dot --title "Initializing database..." -- sqlite3 "$DB_PATH" < "$INIT_SQL"
    if [ $? -eq 0 ]; then
        # Apply update schema
        sqlite3 "$DB_PATH" < "pkm/web/update_schema.sql"
        if [ $? -eq 0 ]; then
            display_success "Database initialized successfully with empty tables."
            gum style --border="rounded" "You can now track:" \
            "- Habits and their completion" \
            "- Alcohol consumption" \
            "- Work hours and projects" \
            "- Daily metrics (mood, energy, sleep)" \
            "- Goals and plans"
            wait_for_key
        else
            display_error "Error applying schema updates."
            wait_for_key
            exit 1
        fi
    else
        display_error "Error initializing database."
        wait_for_key
        exit 1
    fi
}

# Function to get formatted timestamp
get_formatted_timestamp() {
    date "+pkmdb_%B_%d_%Y_%I%M%p"
}

# Function to get machine readable timestamp
get_machine_timestamp() {
    date "+%Y%m%d"
}

# Function to backup database
backup_db() {
    mkdir -p "$BACKUP_DIR"
    TIMESTAMP=$(get_formatted_timestamp)
    BACKUP_PATH="$BACKUP_DIR/${TIMESTAMP}.db"
    
    if [ -f "$DB_PATH" ]; then
        gum spin --spinner dot --title "Creating database backup..." -- cp "$DB_PATH" "$BACKUP_PATH"
        if [ $? -eq 0 ]; then
            display_success "Database backed up to: $BACKUP_PATH"
            get_machine_timestamp > "$LAST_BACKUP_FILE"
            if [ "$1" != "silent" ]; then
                wait_for_key
            fi
        else
            display_error "Error creating backup."
            wait_for_key
            exit 1
        fi
    else
        display_error "Database file not found."
        wait_for_key
        exit 1
    fi
}

# Function to restore database
restore_db() {
    if [ ! -d "$BACKUP_DIR" ]; then
        display_error "No backups directory found."
        wait_for_key
        exit 1
    fi

    # List available backups with most recent first
    echo "Available backups (most recent first):"
    BACKUPS=($(ls -1t "$BACKUP_DIR"))
    SELECTED=$(gum choose "Cancel restore" "${BACKUPS[@]}")
    
    if [ "$SELECTED" = "Cancel restore" ]; then
        echo "Database restore cancelled."
        wait_for_key
        return
    fi
    
    if gum confirm "Are you sure you want to restore from $SELECTED?"; then
        # Create a backup of current database before restore
        echo "Creating backup of current database before restore..."
        backup_db "silent"
        
        # Restore the selected backup
        gum spin --spinner dot --title "Restoring from backup..." -- cp "$BACKUP_DIR/$SELECTED" "$DB_PATH"
        if [ $? -eq 0 ]; then
            display_success "Database restored successfully from: $SELECTED"
            wait_for_key
        else
            display_error "Error restoring database."
            wait_for_key
            exit 1
        fi
    else
        echo "Database restore cancelled."
        wait_for_key
    fi
}

# Function to check for daily backup
check_daily_backup() {
    mkdir -p "$BACKUP_DIR"
    
    if [ ! -f "$LAST_BACKUP_FILE" ]; then
        echo "No previous backup found. Creating initial backup..."
        backup_db "silent"
        return
    fi
    
    LAST_BACKUP_DATE=$(cat "$LAST_BACKUP_FILE")
    TODAY=$(get_machine_timestamp)
    
    if [[ "$LAST_BACKUP_DATE" != "$TODAY" ]]; then
        echo "Creating daily backup..."
        backup_db "silent"
    fi
}

# Function to check if web interface is enabled and get port
check_web_config() {
    if [ ! -f "pkm/web/config.json" ]; then
        display_error "Web configuration file not found."
        return 1
    fi
    
    # Check if web is enabled
    if ! grep -q '"web_enabled": true' "pkm/web/config.json"; then
        display_error "Web interface is not enabled in config. Please enable it in pkm/web/config.json first."
        return 1
    fi
    
    # Extract port number from config
    PORT=$(grep -o '"port": [0-9]*' "pkm/web/config.json" | grep -o '[0-9]*')
    if [ -z "$PORT" ]; then
        display_error "Could not determine port from config."
        return 1
    fi
    
    echo "$PORT"
    return 0
}

# Function to check and handle existing Flask processes
check_flask_processes() {
    # Get configured port
    PORT=$(check_web_config)
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # Check if port is in use
    if netstat -tuln | grep -q ":$PORT "; then
        # Get PIDs of processes using the port
        port_pids=$(lsof -t -i:$PORT)
        if [ ! -z "$port_pids" ]; then
            echo "Found processes using port $PORT:"
            for pid in $port_pids; do
                # Check if this PID belongs to a PKM process
                if ps -p $pid -o cmd= | grep -q "python3 -m pkm.web.app"; then
                    if gum confirm "PKM web server already running (PID: $pid). Would you like to stop it and start a new instance?"; then
                        echo "Stopping PKM web server..."
                        kill $pid
                        sleep 1
                        # Force kill if still running
                        if ps -p $pid > /dev/null; then
                            kill -9 $pid
                        fi
                        return 0
                    else
                        echo "Keeping existing PKM web server running."
                        exit 0
                    fi
                fi
            done
            display_error "Port $PORT is in use by non-PKM process(es). Please either free up port $PORT or change the port in web config."
            exit 1
        fi
    fi
    
    # Check for any other Flask processes that might not be bound to port yet
    existing_pids=$(pgrep -f "python3 -m pkm.web.app")
    if [ ! -z "$existing_pids" ]; then
        echo "Found existing Flask processes:"
        ps -p $existing_pids -o pid,cmd
        if gum confirm "Would you like to kill these processes?"; then
            echo "Killing existing processes..."
            kill $existing_pids
            sleep 1
            # Double check if any processes are still hanging
            if pgrep -f "python3 -m pkm.web.app" > /dev/null; then
                echo "Force killing remaining processes..."
                pkill -9 -f "python3 -m pkm.web.app"
            fi
            echo "All existing processes have been terminated."
        else
            echo "Keeping existing processes running."
            echo "Warning: Starting a new instance might cause port conflicts."
        fi
    fi
}

# Install gum if not present
check_gum

# Check for daily backup before processing any command
check_daily_backup

# Check command line arguments
case "$1" in
    "web")
        PORT=$(check_web_config)
        if [ $? -ne 0 ]; then
            exit 1
        fi
        echo "Checking for existing web instances..."
        check_flask_processes
        echo "Starting web interface on port $PORT..."
        python3 -m pkm.web.app  # Removed gum spin to show Flask logs
        ;;
    "config")
        gum style --foreground="blue" "$EMOJI_CONFIG Opening configuration menu..."
        python3 -m pkm.config_menu
        ;;
    "init-db")
        init_db
        ;;
    "backup-db")
        backup_db
        ;;
    "restore-db")
        restore_db
        ;;
    "backup-md")
        backup_md
        ;;
    "restore-md")
        restore_md
        ;;
    "help")
        show_help
        ;;
    "")
        # Run menu interface (replacing theme selection)
        python3 -m pkm.menu_ui
        ;;
    *)
        display_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac

# Only try to deactivate if we're in a virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi
