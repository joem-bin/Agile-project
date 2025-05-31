from flask import Flask, render_template
import single_operations

app = Flask(__name__)

@app.route('/')
def home():
    items = single_operations.fetch_all()  # Using modular DB functions
    return render_template("home.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)

