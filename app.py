from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
    jsonify,
)
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
    username_exists,
)
from logger import configure_logging
from error_handlers import register_error_handlers
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


configure_logging()
register_error_handlers(app)


@app.context_processor
def inject_user():
    return dict(
        username=session.get("username"),
        user_id=session.get("user_id"),
        role=session.get("role"),
    )


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required.", "error")
            app.logger.warning("Login attempt with missing credentials.")
            return redirect(url_for("home"))

        user = get_user(username, password)

        if user:
            session["user_id"] = user[0]
            session["username"] = username
            session["role"] = user[1]
            app.logger.info(f"User '{username}' logged in successfully.")
            return redirect(url_for("dashboard"))
        else:
            flash("Incorrect username or password.", "error")
            app.logger.warning(f"Login failed for username: {username}")
            return redirect(url_for("home"))

    except Exception:
        app.logger.exception("Unexpected error during login.")
        return render_template("error.html", message="Something went wrong."), 500


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        role = request.form.get("role", "user")

        if not all([username, email, password, confirm_password]):
            flash("All fields are required.", "error")
            app.logger.warning("Signup attempt with missing fields.")
            return render_template("signup.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            app.logger.warning(f"Password mismatch for '{username}'")
            return render_template("signup.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            app.logger.warning(f"Weak password on signup for '{username}'")
            return render_template("signup.html")

        success = insert_user(username, email, password, role)
        if success:
            app.logger.info(f"User '{username}' registered.")
            flash("Account created! Please log in.", "success")
            return redirect(url_for("home"))
        else:
            flash("Username or email already exists.", "error")
            app.logger.warning(f"Signup failed for '{username}' — duplicate.")
            return render_template("signup.html")

    return render_template("signup.html")


@app.route("/check_username")
def check_username():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"exists": False})

    exists = username_exists(username)
    return jsonify({"exists": exists})


# find a way to check this
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in to view the dashboard.", "error")
        app.logger.warning("Unauthorized dashboard access.")
        return redirect(url_for("home"))

    if session["role"] == "admin":
        tickets = get_all_tickets()
    else:
        tickets = get_tickets_for_user(session["user_id"])

    return render_template(
        "admin_dashboard.html" if session["role"] == "admin" else "user_dashboard.html",
        tickets=tickets,
    )


@app.route("/create_ticket", methods=["GET", "POST"])
def create_ticket():
    if "user_id" not in session:
        flash("You must be logged in to create a ticket.", "error")
        return redirect(url_for("home"))

    categories = get_categories()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category_id = request.form.get("category")
        user_id = session["user_id"]

        if not all([title, description, category_id]):
            flash("All fields are required to submit a ticket.", "error")
            app.logger.warning(
                f"Ticket submission failed — missing fields (user {user_id})"
            )
            return render_template(
                "create_ticket.html",
                categories=categories,
                title=title,
                description=description,
                selected_category=category_id,
            )

        try:
            insert_ticket(user_id, category_id, title, description)
            app.logger.info(f"Ticket created by user {user_id}: '{title}'")
            return redirect(
                url_for(
                    "ticket_submitted",
                    title=title,
                    description=description,
                    category=category_id,
                )
            )

        except Exception:
            app.logger.exception(f"Ticket creation failed for user {user_id}")
            flash("Something went wrong while creating your ticket.", "error")
            return render_template(
                "create_ticket.html",
                categories=categories,
                title=title,
                description=description,
                selected_category=category_id,
            )

    return render_template("create_ticket.html", categories=categories)


@app.route("/ticket_submitted")
def ticket_submitted():
    if "user_id" not in session:
        flash("You must be logged in to view this page.", "error")
        return redirect(url_for("home"))

    title = request.args.get("title")
    description = request.args.get("description")
    category = request.args.get("category")

    if not title or not description or not category:
        return redirect(url_for("create_ticket"))

    return render_template(
        "ticket_submitted.html", title=title, description=description, category=category
    )


@app.route("/ticket/<int:ticket_id>")
def ticket_details(ticket_id):
    ticket = get_ticket(ticket_id)
    if not ticket:
        app.logger.warning(f"Ticket {ticket_id} not found.")
        return render_template("error.html", message="Ticket not found."), 404

    comments = get_comments_for_ticket(ticket_id)
    return render_template("ticket_details.html", ticket=ticket, comments=comments)


@app.route("/delete_ticket/<int:ticket_id>", methods=["POST"])
def delete_ticket_route(ticket_id):
    if "user_id" not in session or session["role"] != "admin":
        flash("Only admins can delete tickets.", "error")
        return redirect(url_for("home"))

    delete_ticket(ticket_id)
    app.logger.info(f"Ticket {ticket_id} deleted by admin {session['user_id']}")
    return redirect(url_for("dashboard"))


@app.route("/update_ticket_status/<int:ticket_id>", methods=["POST"])
def update_ticket_status_route(ticket_id):
    if "user_id" not in session or session["role"] != "admin":
        flash("Unauthorized ticket status update attempt.", "error")
        return redirect(url_for("home"))

    new_status = request.form.get("status")
    if new_status not in ["open", "in progress", "closed"]:
        app.logger.warning(f"Invalid ticket status '{new_status}'")
        return redirect(url_for("ticket_details", ticket_id=ticket_id))

    update_ticket_status(ticket_id, new_status)
    app.logger.info(
        f"Ticket {ticket_id} updated to '{new_status}' by admin {session['user_id']}"
    )
    return redirect(url_for("ticket_details", ticket_id=ticket_id))


@app.route("/add_comment", methods=["POST"])
def add_comment():
    if "user_id" not in session:
        flash("You must be logged in to comment.", "error")
        return redirect(url_for("home"))

    ticket_id = request.form.get("ticket_id")
    message = request.form.get("message")
    user_id = session["user_id"]

    if not message or not ticket_id:
        app.logger.warning("Comment submission failed — missing message or ticket ID.")
        return redirect(url_for("ticket_details", ticket_id=ticket_id))

    insert_comment(ticket_id, user_id, message)
    app.logger.info(f"Comment added to ticket {ticket_id} by user {user_id}")
    return redirect(url_for("ticket_details", ticket_id=ticket_id))


@app.route("/confirm_close_ticket/<int:ticket_id>", methods=["POST"])
def confirm_close_ticket(ticket_id):
    if "user_id" not in session:
        flash("You must be logged in to close a ticket.", "error")
        return redirect(url_for("home"))

    close_ticket(ticket_id)
    app.logger.info(f"Ticket {ticket_id} closed by user {session['user_id']}")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    ENV = os.getenv("FLASK_ENV", "production")

    app.debug = ENV == "development"
    app.logger.info(f"Running in {ENV} mode")

    app.run()
