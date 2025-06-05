from flask import Flask, render_template
import single_operations

app = Flask(__name__)

@app.route('/')
def home():
    tickets = single_operations.fetch_all()  # Using modular DB functions
    return render_template("home.html", items=tickets)

if __name__ == "__main__":
    app.run(debug=True)

