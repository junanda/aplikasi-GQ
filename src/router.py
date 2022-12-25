from flask import render_template, url_for, session, redirect, flash
from functools import wraps
from main import app


def authentication(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('you need to login first')
            return redirect(url_for('index'))
    return wrap


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")
