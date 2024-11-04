 #!/bin/bash

set -e
# set -x

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
python3 -m venv pkm_venv

# Activate virtual environment
source pkm_venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "Setup complete. You can now run ./demo.sh to generate demo data."
