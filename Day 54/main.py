from flask import Flask, render_template

app = Flask(__name__)


# -----------------------------
# Python Decorator Example
# -----------------------------

def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"

    return wrapper


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return "<h1>About Page</h1><p>Welcome to my Flask application!</p>"


@app.route("/hello/<name>")
def hello(name):
    return f"<h1>Hello {name}!</h1>"


@app.route("/decorator")
@make_bold
def decorator_example():
    return "This text is modified using a Python decorator!"


if __name__ == "__main__":
    app.run(debug=True)