from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import auth, dashboard, pred_engine


app = Flask(__name__)
app.secret_key = "lansdjkacnkaj1234"

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:triadpass@localhost/gina_cluster'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.register_blueprint(auth.auth)
app.register_blueprint(dashboard.dashboard)

db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)
