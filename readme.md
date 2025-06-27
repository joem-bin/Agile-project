# Flask Helpdesk Ticketing App

## Overview

A Flask-based web application for submitting, managing, and resolving support tickets. Built with SQLite, modularized logic, GOV.UK styling, integrated logging, security scanning, and CI automation.


## Live Demo

This project is deployed and live on Render:  
[https://it-ticket-system-joe-m.onrender.com/dashboard]

Note: It may take a few seconds to wake up after inactivity (free-tier cold start).




---

## Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/joem-bin/Agile-project.git
cd your-repo
```

2. **Create and activate a virtual environment:**

- **Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

- **macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set environment variables:**

Create a `.env` file in the project root. Here's a safe example:

```
FLASK_ENV=development
SECRET_KEY=supersecretkey
DB_NAME=app.db
LOG_DIR=logs
LOG_LEVEL=INFO
LOG_FILE=app.log
```
Never commit `.env` to version control—use `.env.example` for sharing structure.


5. **(Optional) Run logging setup (clears old logs and verifies setup):**


python setup_logs.py

6. **reset the db (puts 10 sample records in the db)**

python setup_db.py
python setup_logs.py


7. **Run the app:**


python app.py

## Testing

### Run tests locally:

```bash
pytest tests
```


### Format + lint before committing:

```bash
black .
flake8
```

### Security scan before pushing:

```bash
bandit -r . -x tests,venv,.venv,__pycache__ -s B101,B311
```

### Lint templates:

```bash
djlint templates/ --check
```


##  Useful Dev Commands

```bash
# Freeze current dependencies into requirements.txt
pip freeze > requirements.txt

# Deactivate the current Python virtual environment
deactivate

# Delete the virtual environment folder
rm -rf .venv        # macOS/Linux
rmdir /s /q .venv   # Windows

# Run Flask locally
python app.py
```

---

## 🛠️ Future Improvements

- [ ] Dockerization for deployable containers  
- [ ] Role-based access control enhancements  
- [ ] Email notifications for ticket updates  
- [ ] Pagination/search for large ticket queues  

