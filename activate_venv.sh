#!/bin/bash

# Check if the virtual environment directory exists
if [ -d "venv" ]; then
    # Activate the virtual environment
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Virtual environment 'venv' does not exist."
    echo "Please create it using 'python -m venv venv'"
fi

