from flask import Blueprint, render_template, jsonify, request
from ..tools import authentication
from ..main import db
from scipy.spatial.distance import euclidean


ujimetode = Blueprint("ujimodel", __name__, url_prefix="/testing")

#index ujimodel
@ujimetode.route('/', methods=['GET', 'POST'])
@authentication
def index():
    l_active = 'active'
    return render_template('ujimetode_view.html', active_f=l_active)

@ujimetode.route('/calculate', methods=['POST','GET'])
def calculate_predict():
    data_model = dict()
    calculate_data = request.get_json()
    label_1 = 0
    label_2 = 0

    data_calculasi = db.engine.execute("select nilai_skp, orientasi, integritas, komitmen, disiplin, kerjasama, label from nilai_aspek_pegawai where label !=''").fetchall()
    
    data_test = [float(val) for n, val in calculate_data['data'].items()]
    
    for i, row in enumerate(data_calculasi):
        data_model[f"Data_{i+1}"] = {"value":[row.nilai_skp, row.orientasi, row.integritas, row.komitmen, row.disiplin, row.kerjasama],"label":row.label}
    
    nilai_jarak = []
    # menghitung jarak antara dokument
    for doc in data_model.items():
        nilai_jarak.append({"dokumen": doc[0], "jarak": euclidean(doc[1]['value'], data_test[:-1]), 'label': doc[1]['label']})

    # sorting berdasarkan nilai yang terdekat/terkecil
    doc_sort = sorted(nilai_jarak, key=lambda x:x['jarak'])

    # mengambil doc ketetanggaan yang terdekat
    tetangga_doc = doc_sort[:int(data_test[-1])]
    print(tetangga_doc)
    
    label = ''
    # penentuan label data
    for n in tetangga_doc:
        if n['label'] == '0':
            label_1 += 1
        else:
            label_2 += 1
    
    if label_1 > label_2:
        label = 'Layak'
    else:
        label = 'Tidak Layak'
    
    data_result = {"nama":calculate_data['nama'], "label": label, "jumlah_ketetanggaan": data_test[-1], "jarak_minimum": doc_sort[0]['jarak'], "jarak_maksimum":doc_sort[-1]['jarak']}

    resutl = jsonify({"message":"success", "data": data_result})
    return resutl
