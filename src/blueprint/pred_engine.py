from flask import Blueprint, render_template, request, json, jsonify
from ..tools import authentication
from ..main import db
from ..main import model_knn
import pandas as pd


predict = Blueprint('predict', __name__, url_prefix='/predict')


# index predict
@predict.route('/', methods=['GET', 'POST'])
@authentication
def index():
    l_active = 'active'
    all_data = db.engine.execute("select * from nilai_aspek_pegawai where label !='' ").fetchall()
    train = int(len(all_data) * 0.8)
    test = int(len(all_data)*0.2)
    if request.method == 'POST':
        predict = 'kompeten'
        data_test = pd.DataFrame(columns=['NILAI SKP', 'ORIENTASI', 'INTEGRITAS', 'KOMITMEN', 'DISIPLIN', 'KERJASAMA'])
        data_test = [
            [
                float(request.form['nilai_skp']),
                float(request.form['orientasi']),
                float(request.form['integritas']),
                float(request.form['komitmen']),
                float(request.form['disiplin']),
                float(request.form['kerjasama'])
            ]
        ]
        result_prediksi = model_knn.predict(data_test)
        del data_test
        if result_prediksi[0] != 0:
            predict = 'tidak kompeten'

        return render_template(
            'classification_view.html', 
            active_e=l_active,
            alldata=len(all_data),
            data_train=train,
            data_test=test,
            predict=predict   
        )
    return render_template(
        'classification_view.html', 
        active_e=l_active,
        alldata=len(all_data),
        data_train=train,
        data_test=test
        )

# predict classification
@predict.route('/load-file', methods=['POST'])
def readFileExcel():
    response = any
    file = request.files['file']
    data = pd.read_excel(file)
    data_ex = data.to_json(orient="records")
    parsed = json.loads(data_ex)
    print(parsed[1:])
    response = jsonify({"message": "success", "data": parsed})
    response.status_code = 200

    return response

# show class predict
