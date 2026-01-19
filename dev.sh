#!/bin/bash
set -e

# Update environment variables
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/trusted_pay"

# initiate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# run the development server
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload