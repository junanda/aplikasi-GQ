from flask import render_template, url_for, session, redirect, flash, Blueprint, request
from src.model import Admin
from src.main import db
from passlib.hash import bcrypt
import gc


auth = Blueprint('auth', __name__, url_prefix="/")

# @auth.route("/", methods=("POST", "GET"))
# def index():
#     print("home")
#     return render_template("index.html")


@auth.route('/')
@auth.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_get = Admin.query.filter_by(username=username).first()

        if admin_get and bcrypt.verify(password, admin_get.password):
            session.clear()
            session['name'] = admin_get.name
            session['logged_in'] = True
            return redirect(url_for('dashboard.index'))

        else:
            flash('use username or password correct')
            return redirect(url_for('auth.login'))

    return render_template('index.html')


@auth.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = bcrypt.encrypt(request.form['password'])

        add_user = Admin(name, username, password)
        db.session.add(add_user)
        db.session.commit()
        flash('new admin success to registered')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
# @authentication
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    session.clear()
    flash('logged out')
    gc.collect()
    return redirect(url_for('auth.login'))
