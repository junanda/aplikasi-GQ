from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = "lansdjkacnkaj1234"

    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:triadpass@localhost/gina_cluster'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    from .blueprint import auth, dashboard
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)

    return app
# if __name__ == "__main__":

#     app.run(debug=True)
