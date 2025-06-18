from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from database_operations import (
    insert_ticket,
    get_user,
    get_tickets_for_user,
    get_all_tickets,
    get_ticket,
    get_comments_for_ticket,
    get_categories,
    close_ticket,
    insert_comment,
    delete_ticket, 
    update_ticket_status,
    insert_user,
    username_exists
)
from logger import configure_logging
from error_handlers import register_error_handlers
import os
from dotenv import load_dotenv
load_dotenv()






app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


configure_logging()
register_error_handlers(app)

@app.context_processor
def inject_user():
    return dict(
        username=session.get('username'),
        user_id=session.get('user_id'),
        role=session.get('role')
    )

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash("Username and password are required.", "error")
            app.logger.warning("Login attempt with missing credentials.")
            return redirect('/')

        user = get_user(username, password)

        if user:
            session['user_id'] = user[0]
            session['username'] = username
            session['role'] = user[1]
            app.logger.info(f"User '{username}' logged in successfully.")
            return redirect('/dashboard')
        else:
            flash("Incorrect username or password.", "error")
            app.logger.warning(f"Login failed for username: {username}")
            return redirect('/')

    except Exception as e:
        app.logger.exception("Unexpected error during login.")
        return render_template("error.html", message="Something went wrong."), 500

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        role = request.form.get('role', 'user')

        if not all([username, email, password, confirm_password]):
            flash("All fields are required.", "error")
            app.logger.warning("Signup attempt with missing fields.")
            return render_template('signup.html')

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            app.logger.warning(f"Password mismatch for '{username}'")
            return render_template('signup.html')

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            app.logger.warning(f"Weak password on signup for '{username}'")
            return render_template('signup.html')

        success = insert_user(username, email, password, role)
        if success:
            app.logger.info(f"User '{username}' registered.")
            flash("Account created! Please log in.", "success")
            return redirect('/')
        else:
            flash("Username or email already exists.", "error")
            app.logger.warning(f"Signup failed for '{username}' — duplicate.")
            return render_template('signup.html')

    return render_template('signup.html')




@app.route('/check_username')
def check_username():
    username = request.args.get('username', '').strip()
    if not username:
        return jsonify({'exists': False})
    
    exists = username_exists(username)
    return jsonify({'exists': exists})





@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    if session['role'] == 'admin':
        tickets = get_all_tickets()
    else:
        tickets = get_tickets_for_user(session['user_id'])

    return render_template(
        'admin_dashboard.html' if session['role'] == 'admin' else 'user_dashboard.html',
        tickets=tickets
    )

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if 'user_id' not in session:
        return redirect('/')

    categories = get_categories()  

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category_id = request.form['category']
        user_id = session['user_id']

        insert_ticket(user_id, category_id, title, description)

        return redirect(url_for('ticket_submitted', title=title, description=description, category=category_id))

    return render_template('create_ticket.html', categories=categories)  

@app.route('/ticket_submitted')
def ticket_submitted():
    if 'user_id' not in session:
        return redirect('/')

    title = request.args.get('title')
    description = request.args.get('description')
    category = request.args.get('category')

    if not title or not description or not category:
        return redirect(url_for('create_ticket'))

    return render_template('ticket_submitted.html', title=title, description=description, category=category)

@app.route('/ticket/<int:ticket_id>')
def ticket_details(ticket_id):
    ticket = get_ticket(ticket_id)
    comments = get_comments_for_ticket(ticket_id)

    return render_template('ticket_details.html', ticket=ticket, comments=comments)

@app.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
def delete_ticket_route(ticket_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect('/')

    delete_ticket(ticket_id)
    return redirect('/dashboard')

@app.route('/update_ticket_status/<int:ticket_id>', methods=['POST'])
def update_ticket_status_route(ticket_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect('/')

    new_status = request.form.get('status')
    if new_status not in ['open', 'in progress', 'closed']:
        return redirect(url_for('ticket_details', ticket_id=ticket_id))  

    update_ticket_status(ticket_id, new_status)
    return redirect(url_for('ticket_details', ticket_id=ticket_id))

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return redirect('/')

    ticket_id = request.form.get('ticket_id')
    message = request.form.get('message')
    user_id = session['user_id']

    if not message or not ticket_id:
        return redirect(url_for('ticket_details', ticket_id=ticket_id))

    insert_comment(ticket_id, user_id, message)

    return redirect(url_for('ticket_details', ticket_id=ticket_id))

@app.route('/confirm_close_ticket/<int:ticket_id>', methods=['POST'])
def confirm_close_ticket(ticket_id):
    if 'user_id' not in session:
        return redirect('/')

    close_ticket(ticket_id)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    ENV = os.getenv("FLASK_ENV", "production")

    app.debug = ENV == "development"
    app.logger.info(f"Running in {ENV} mode")

    app.run()

