from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management
DB_NAME = "test.db"

# Function to connect to the database
def get_db_connection():
    return sqlite3.connect(DB_NAME)

# landing page
@app.route('/')
def home():
    return render_template('login.html')

# login functionality --> could add new user registration here
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, role FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        session['role'] = user[1]
        return redirect('/dashboard')
    else:
        return render_template('error.html', message="Invalid credentials!")


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    if session['role'] == 'admin':
        cursor.execute("SELECT * FROM tickets")
    else:
        cursor.execute("SELECT * FROM tickets WHERE user_id = ?", (session['user_id'],))

    tickets = cursor.fetchall()
    conn.close()

    return render_template(
        'admin_dashboard.html' if session['role'] == 'admin' else 'user_dashboard.html',
        tickets=tickets
    )

@app.route('/ticket/<int:ticket_id>')
def ticket_details(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    ticket = cursor.fetchone()

    cursor.execute("SELECT * FROM comments WHERE ticket_id = ?", (ticket_id,))
    comments = cursor.fetchall()
    conn.close()

    return render_template('ticket_details.html', ticket=ticket, comments=comments)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
