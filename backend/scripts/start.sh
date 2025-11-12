#!/bin/bash

# Start script for the application

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements/dev.txt
else
    source .venv/bin/activate
fi

# Start the application
echo "Starting the application..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000