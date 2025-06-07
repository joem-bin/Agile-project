from flask import Flask, render_template, request, redirect, session, url_for
from database_operations import (
    insert_ticket,
    get_user,
    get_tickets_for_user,
    get_all_tickets,
    get_ticket,
    get_comments
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = get_user(username, password)

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

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category_id = request.form['category']
        user_id = session['user_id']

        insert_ticket(user_id, category_id, title, description)

        return redirect(url_for('ticket_submitted', title=title, description=description, category=category_id))

    return render_template('create_ticket.html')

@app.route('/ticket_submitted')
def ticket_submitted():
    if 'user_id' not in session:
        return redirect('/')

    title = request.args.get('title')
    description = request.args.get('description')
    category = request.args.get('category')

    if not title or not description or not category:
        # Missing info, redirect to create_ticket
        return redirect(url_for('create_ticket'))

    return render_template('ticket_submitted.html', title=title, description=description, category=category)

@app.route('/ticket/<int:ticket_id>')
def ticket_details(ticket_id):
    ticket = get_ticket(ticket_id)
    comments = get_comments(ticket_id)

    return render_template('ticket_details.html', ticket=ticket, comments=comments)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
