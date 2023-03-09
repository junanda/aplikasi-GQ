from flask import Blueprint, render_template, request, json, jsonify
from ..tools import authentication
from ..main import db
from ..main import model_knn
from scipy.spatial.distance import euclidean
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
    name_col = ['no','nama', 'nilai_skp', 'orientasi', 'integritas', 'komitmen', 'disiplin', 'kerjasama']
    response = any
    file = request.files['file']
    data = pd.read_excel(file)
    data.columns = name_col
    data_ex = data.to_json(orient="records")
    parsed = json.loads(data_ex)
    response = jsonify({"message": "success", "data": parsed})
    response.status_code = 200
    del data
    del data_ex
    return response

@predict.route('/calculate', methods=['POST', 'GET'])
def calculate_distance():
    response = any
    data_model = dict()
    data_req = request.get_json()
    columns = ["id_aspek","nilai_skp","orientasi","integritas","komitmen","disiplin","kerjasama","label"]
    data_label = db.engine.execute("select nilai_skp, orientasi, integritas, komitmen, disiplin, kerjasama, label from nilai_aspek_pegawai where label !=''").fetchall()

    for idex, row in enumerate(data_label):
        data_model[f"Data_{idex + 1}"] = {"value":[row.nilai_skp, row.orientasi, row.integritas, row.komitmen, row.disiplin, row.kerjasama],"label":row.label}
    
    hasil_data = transformDataReq(data_req['data'])
    result_calculate = hitungJarak(data_model, hasil_data)
    
    response = jsonify({"message": "success", "data": result_calculate, "informasi":"Data hasil perhitungan jarak dengan euclidean"})

    return response

def transformDataReq(data):
    result = []
    for dat in data:
        result.append([
            dat['nama'],
            dat['nilai_skp'],
            dat['orientasi'],
            dat['integritas'],
            dat['komitmen'],
            dat['disiplin'],
            dat['kerjasama'],
            ])
    return result

def hitungJarak(dataDoc, datafile):
    result = []

    for n in datafile:
        val_distance = []
        for doc in dataDoc.items():
            val_distance.append({"dokumen": doc[0],"distance": euclidean(doc[1]['value'], n[1:]), 'label': doc[1]['label']}) 
        result.append({'nama': n[0],'detail': val_distance})
    return result