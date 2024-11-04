# File Guide

This document provides a comprehensive overview of all files in the PKM system and their purposes.

## Root Directory Files

### Core Documentation
- **README.md**: Main project documentation with system overview and setup instructions
- **QUICKSTART.md**: Condensed guide for quick system setup and basic usage
- **WISHLIST.md**: Planned features and future development roadmap
- **AI_GUIDE.md**: Development guidelines for AI assistance in maintaining the system
- **FILE_GUIDE.md**: This file - documents the purpose of each file in the project

### Setup and Installation
- **install.sh**: Complete system installation script (dependencies, virtual env, database)
- **setup.sh**: Basic setup script (alternative to install.sh)
- **venv.sh**: Virtual environment management script
- **requirements.txt**: Python package dependencies

### Core Scripts
- **pkm.sh**: Main application launcher script
- **check_db.py**: Database verification and maintenance script
- **get_date_range.py**: Utility for date range operations
- **setup.py**: Python package setup configuration

### Utility Scripts
- **cleanup.sh**: System maintenance and cleanup operations
- **demo.sh**: Demo data generation script
- **truncate_demo.sh**: Script to clean demo data
- **git_push_commit_merge.sh**: Git operations automation script
- **h_commit_merge.sh**: Alternative git operations script
- **start-pkm.sh**: Quick start script for the PKM system

## PKM Directory (/pkm)

### Core Python Modules
- **pkm_manager.py**: Main system management class
- **pkm_cli.py**: Command-line interface implementation
- **menu_ui.py**: Terminal menu interface
- **utils.py**: Utility functions and helpers
- **config_menu.py**: Configuration interface
- **themes.py**: Theme management system
- **generate_demo_data.py**: Demo data generation utilities

### Configuration
- **theme_config.json**: Theme configuration settings
- **__init__.py**: Python package initialization

### Web Interface (/pkm/web)
- **app.py**: Web application server
- **config.json**: Web interface configuration
- **configure.py**: Web interface setup utilities
- **update_schema.sql**: Database schema updates

### Templates
- **templates/daily_template.md**: Template for daily log entries
- **web/templates/*.html**: Web interface HTML templates
  - base.html: Base template with common elements
  - index.html: Main dashboard
  - login.html: Authentication page
  - daily_logs.html: Daily logs view
  - edit_log.html: Log editing interface
  - habits.html: Habits tracking interface
  - metrics.html: Metrics visualization
  - work.html: Work logging interface
  - alcohol.html: Alcohol consumption tracking

### Database (/pkm/db)
- **init.sql**: Database initialization schema
- **.last_backup**: Timestamp of last backup
- **backups/**: Database backup storage
- **md_backups/**: Markdown file backups

## Data Directories

### Daily Logs
- **daily/**: Storage for daily markdown logs
- **daily/.gitignore**: Git ignore rules for daily logs

### Database
- **db/**: Main database storage
- **db/init.sql**: Database initialization
- **db/backups/**: Database backup storage
- **db/backups/.gitignore**: Git ignore rules for backups

## Version Control
- **.gitignore**: Git ignore rules
- **.version_tracker**: Version tracking file

## Usage Examples

### Creating a Daily Log
```bash
./pkm.sh daily
```
This uses daily_template.md to create a new daily log in the daily/ directory.

### Running the Web Interface
```bash
./pkm.sh web
```
This launches the Flask web server (app.py) with the configured templates.

### Database Operations
```bash
./pkm.sh init-db    # Initialize database using init.sql
./pkm.sh backup-db  # Create backup in db/backups/
./pkm.sh restore-db # Restore from latest backup
```

## File Organization Principles

1. **Separation of Concerns**
   - Core functionality in /pkm
   - User data in /daily and /db
   - Configuration in JSON files
   - Templates separate from code

2. **Data Management**
   - Database files in dedicated directories
   - Regular backup locations defined
   - Clear separation of user data

3. **Interface Organization**
   - CLI tools in root directory
   - Web interface in dedicated directory
   - Templates organized by interface type

4. **Documentation Structure**
   - User guides in root directory
   - Technical documentation with code
   - Clear naming conventions
