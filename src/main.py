from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
config = {
    'DEBUG': True,
}


def create_app():
    app = Flask(__name__)
    app.secret_key = "lansdjkacnkaj1234"

    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:triadpass@localhost/gina_cluster'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    app.config.from_mapping(config)

    from .blueprint import auth, dashboard
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)

    return app


if __name__ == "__main__":
    cap = create_app()
    cap.run(debug=True)
