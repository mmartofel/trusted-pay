# Ensure your python path sees the current directory
export PYTHONPATH=$PYTHONPATH:.

# Update postgres environment variables
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/trusted_pay"

# initiate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the initialization
python3 init_db.py
