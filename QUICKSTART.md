# Quick Start Guide

## Installation

1. Install system requirements:
```bash
# For Debian/Ubuntu
sudo apt-get update
sudo apt-get install python3 python3-pip sqlite3
```

2. Run the installation script:
```bash
./install.sh
```

3. Activate the virtual environment:
```bash
source venv.sh activate
```

## Available Shell Scripts

### Essential Scripts
1. **install.sh**
   ```bash
   ./install.sh  # Full system installation
   ```

2. **venv.sh**
   ```bash
   source venv.sh activate    # Activate virtual environment
   source venv.sh deactivate  # Deactivate virtual environment
   source venv.sh help        # Show all scripts documentation
   ```

3. **pkm.sh**
   ```bash
   ./pkm.sh              # Terminal Interface
   ./pkm.sh web         # Web Interface
   ./pkm.sh config      # Configuration Menu
   ./pkm.sh help        # Show Help
   ./pkm.sh init-db     # Initialize database
   ./pkm.sh backup-db   # Create database backup
   ./pkm.sh restore-db  # Restore database
   ./pkm.sh backup-md   # Backup markdown files
   ./pkm.sh restore-md  # Restore markdown files
   ```

### Additional Scripts
4. **setup.sh**
   ```bash
   ./setup.sh  # Basic setup (alternative to install.sh)
   ```

5. **demo.sh**
   ```bash
   ./demo.sh  # Generate sample data
   ```

6. **cleanup.sh**
   ```bash
   ./cleanup.sh  # System cleanup and maintenance
   ```

[Rest of QUICKSTART.md content remains unchanged from here...]

Quick

TODO: Add documentation for this section

Start

TODO: Add documentation for this section

Guide

TODO: Add documentation for this section

Prerequisites

TODO: Add documentation for this section

Setup

TODO: Add documentation for this section

Running

TODO: Add documentation for this section
