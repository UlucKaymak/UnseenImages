#!/bin/bash

# Define paths
VENV_PATH="/home/username/Projects/TwitterBot/_env_twitterbot/bin"
PYTHON_SCRIPT="/media/username/RPIPROJECTS/twitterbot/run_app.py"
LOG_FILE="/media/username/RPIPROJECTS/twitterbot/cron.log"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Run the Python script and log output
python "$PYTHON_SCRIPT" > "$LOG_FILE" 2>&1

# Deactivate the virtual environment
deactivate