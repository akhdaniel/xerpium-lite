#!/bin/bash

# Activate the Python virtual environment
source backend/.venv/bin/activate

# Start the FastAPI backend using uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
