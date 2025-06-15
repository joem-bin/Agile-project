from flask import Flask, render_template, request, redirect, session, url_for 
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
    insert_user
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

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
    username = request.form['username']
    password = request.form['password']

    user = get_user(username, password)  # Assuming this returns user details

    if user:
        session['user_id'] = user[0]
        session['username'] = username  # Store username
        session['role'] = user[1]
        return redirect('/dashboard')
    else:
        return render_template('error.html', message="Invalid credentials!")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        if password != confirm_password:
            return render_template('error.html', message="Passwords do not match!")

        success = insert_user(username, email, password, role)

        if success:
            return redirect('/')
        else:
            return render_template('error.html', message="Username or Email already exists!")

    return render_template('signup.html')

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
    app.run(debug=True)
