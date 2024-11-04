#!/bin/bash

set -e
# set -x

# Color definitions
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to create a backup
create_backup() {
    backup_dir="pkm_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir "$backup_dir"
    
    # Backup database
    if [ -f "pkm/db/pkm.db" ]; then
        cp "pkm/db/pkm.db" "$backup_dir/"
    fi
    
    # Backup markdown files
    if [ -d "daily" ]; then
        cp -r "daily" "$backup_dir/"
    fi
    
    echo "Backup created in $backup_dir"
}

# First, check if virtual environment exists and activate it
if [ ! -d "pkm_venv" ]; then
    echo -e "${BLUE}Virtual environment not found. Running install.sh...${NC}"
    ./install.sh
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to run install.sh. Please check the error messages above.${NC}"
        exit 1
    fi
fi

# Source the virtual environment script
echo -e "${BLUE}Activating virtual environment...${NC}"
source ./venv.sh activate

# Verify the virtual environment is working
if [ ! -f "pkm_venv/bin/python" ]; then
    echo -e "${RED}Error: Virtual environment Python not found at pkm_venv/bin/python${NC}"
    echo -e "${BLUE}Running install.sh to fix the environment...${NC}"
    ./install.sh
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to run install.sh. Please check the error messages above.${NC}"
        exit 1
    fi
    source ./venv.sh activate
fi

# Check for existing data
if [ -f "pkm/db/pkm.db" ] || [ -d "daily" ]; then
    echo -e "${BLUE}Warning: Existing data detected.${NC}"
    read -p "Do you want to proceed? This will overwrite existing data. (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled."
        exit 1
    fi
    
    read -p "Do you want to create a backup of your existing data? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_backup
    fi
fi

# Ensure pkm/db directory exists
mkdir -p pkm/db

# Ask user for time period type
echo -e "${BLUE}Would you like to generate demo data for:${NC}"
echo "1) Days"
echo "2) Months"
read -p "Enter your choice (1 or 2): " period_choice

case $period_choice in
    1)
        echo "How many days of demo data would you like to generate?"
        echo "Recommended: 3-7 days"
        read -p "Enter number of days (default is 3): " days
        
        # Use default if no input
        if [ -z "$days" ]; then
            days=3
        fi
        
        # Validate input is a positive number
        if ! [[ "$days" =~ ^[0-9]+$ ]] || [ "$days" -lt 1 ]; then
            echo -e "${RED}Error: Please enter a positive number${NC}"
            exit 1
        fi
        
        # Create temporary Python script for days calculation
        cat > temp_demo_calc.py << 'EOF'
import sys
days = int(sys.argv[1])
months = days / 30.0
print(f"{months:.6f}")
EOF
        
        # Convert days to months for the generator
        months=$("pkm_venv/bin/python" temp_demo_calc.py "$days")
        rm temp_demo_calc.py
        ;;
    2)
        echo "How many months of demo data would you like to generate?"
        echo "Note: More months will increase the demo_data.json file size."
        echo "Recommended: 1-3 months"
        read -p "Enter number of months (default is 3): " months
        
        # Use default if no input
        if [ -z "$months" ]; then
            months=3
        fi
        
        # Validate input is a positive number
        if ! [[ "$months" =~ ^[0-9]+$ ]] || [ "$months" -lt 1 ]; then
            echo -e "${RED}Error: Please enter a positive number${NC}"
            exit 1
        fi
        ;;
    *)
        echo -e "${RED}Error: Invalid choice${NC}"
        exit 1
        ;;
esac

# Run the demo data generation and import script using the virtual environment's Python
if [ "$period_choice" = "1" ]; then
    echo -e "${BLUE}Generating $days day(s) of demo data...${NC}"
else
    echo -e "${BLUE}Generating $months month(s) of demo data...${NC}"
fi

"pkm_venv/bin/python" pkm/generate_demo_data.py "$months"
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to generate demo data.${NC}"
    exit 1
fi

echo -e "${GREEN}Demo data has been generated and imported into the PKM database.${NC}"
echo -e "${GREEN}You can now view the demo data in the WebUI.${NC}"
