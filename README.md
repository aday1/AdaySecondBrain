# Personal Knowledge Management (PKM) System

A comprehensive personal knowledge management system that combines Markdown notes with SQLite database tracking for various personal metrics. Access your data through both a terminal interface and an optional web interface.

## Shell Scripts Overview

The system includes several shell scripts for different purposes:

### Core Scripts
1. **install.sh**
   - Main installation script
   - Checks Python installation
   - Creates virtual environment
   - Installs requirements
   - Initializes databases
   - Sets up directory structure

2. **setup.sh**
   - Basic setup script (simpler alternative to install.sh)
   - Creates virtual environment
   - Installs requirements

3. **pkm.sh**
   - Main application launcher
   - Commands:
     - `./pkm.sh web` - Start web interface
     - `./pkm.sh config` - Open configuration menu
     - `./pkm.sh init-db` - Initialize database
     - `./pkm.sh backup-db` - Create database backup
     - `./pkm.sh restore-db` - Restore database
     - `./pkm.sh backup-md` - Backup markdown files
     - `./pkm.sh restore-md` - Restore markdown files

### Utility Scripts
4. **venv.sh**
   - Manages Python virtual environment
   - Commands:
     - `source venv.sh activate` - Activate virtual environment
     - `source venv.sh deactivate` - Deactivate virtual environment
     - `source venv.sh help` - Show help about all scripts

5. **demo.sh**
   - Generates sample data for testing
   - Creates backups before generating demo data
   - Allows specifying months of demo data

6. **cleanup.sh**
   - System cleanup and maintenance
   - Removes Python bytecode files
   - Cleans virtual environment
   - Manages database backups
   - Cleans daily markdown files

## Installation

1. Install system dependencies:
```bash
# For Debian/Ubuntu
sudo apt-get update
sudo apt-get install python3 python3-pip sqlite3

# For Fedora
sudo dnf install python3 python3-pip sqlite3

# For Arch Linux
sudo pacman -S python python-pip sqlite
```

2. Run the installation script:
```bash
./install.sh
```

3. Activate the virtual environment:
```bash
source venv.sh activate
```

[Rest of README.md content remains unchanged from here...]

Description

TODO: Add documentation for this section

Installation

TODO: Add documentation for this section

Usage

TODO: Add documentation for this section

Configuration

TODO: Add documentation for this section
