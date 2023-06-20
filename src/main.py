from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import joblib

global model_knn

db = SQLAlchemy()
config = {
    'DEBUG': True,
}

userDb = os.getenv("USER_DB")
passDB = os.getenv("PASS_DB")
host = os.getenv("HOST_DB")
dbName = os.getenv("NAME_DB")

model_tmp = 'model_train/knn_model_v1.0.sav'

def load_model(name_model):
    return joblib.load(open(name_model, 'rb'))

model_knn = load_model(model_tmp)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.secret_key = "lansdjkacnkaj1234"

    app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{userDb}:{passDB}@{host}/{dbName}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    app.config.from_mapping(config)

    from .blueprint import auth, dashboard, bpegawai, clustering, predict, ujimetode
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(bpegawai)
    app.register_blueprint(clustering)
    app.register_blueprint(predict)
    app.register_blueprint(ujimetode)

    return app


if __name__ == "__main__":
    cap = create_app()
    cap.run(debug=True)
