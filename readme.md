# Flask Web App

## Overview
A simple Flask web application that serves HTML pages and uses SQLite as the database.

## Setup Instructions
1. Clone the repository: `git clone `

2. Create and activate a virtual environment:  
   - **Windows:** `python -m venv .venv && .venv\Scripts\activate`
   - **macOS/Linux:** `python -m venv .venv && source .venv/bin/activate`

3. Install dependencies: `pip install -r requirements.txt`

4. Run the Flask app: `python app.py` or `flask run`

5. (Optional) Initialize SQLite database: `python -c "from app import db; db.create_all()"`


## Useful Commands
- Check installed dependencies: `pip freeze`
- Update `requirements.txt`: `pip freeze > requirements.txt`
- Deactivate virtual environment: `deactivate`
- Remove virtual environment: `rm -rf .venv` (Mac/Linux) or `rmdir /s /q .venv` (Windows)
- install  dependencies `pip install -r requirements.txt`

## Future Improvements
Consider Dockerisation, 
authentication,
more db tables,
better design for front end,
make a github project

