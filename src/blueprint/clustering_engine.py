from flask import Blueprint, render_template, redirect, url_for, request, json, jsonify
from flask_cors import cross_origin
from fileinput import filename
from ..tools import authentication
from ..main import db
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
import pandas as pd


clustering = Blueprint('clustering', __name__, url_prefix='/clustering')

centroid = [
    [88.94495413, 87.55862385, 85.73568807, 85.65174312, 86.28036697, 86.05045872],
    [85.63931034, 81.24386207, 81.11351724, 80.83731034, 81.03634483, 80.83289655]
]

col_cal = ['nilai_skp', 'orientasi', 'integritas', 'komitmen', 'disiplin', 'kerjasama']

#index
@clustering.route('/', methods=('GET','POST'))
@authentication
def index():
    l_active = 'active'
    # query untuk mengambil seluruh data nilai_aspek_pegawai
    query2 = "select * from nilai_aspek_pegawai where label !=''"
    countRow = db.engine.execute(query2).fetchall()
    
    allData = db.engine.execute("select * from nilai_aspek_pegawai").fetchall()

    dataCluster1 = db.engine.execute("select * from nilai_aspek_pegawai where label='0'").fetchall()
    dataCluster2 = len(countRow) - len(dataCluster1)
    data_no_label = len(allData) - len(countRow)
    return render_template(
            'clustering_view.html', 
            active_d=l_active,
            numberAllData=len(allData),
            dataCluster=len(countRow),
            clus_1=len(dataCluster1),
            clus_2=dataCluster2,
            no_label= data_no_label
        )

#show data clustering
#train model
@clustering.route('/train', methods=['POST', 'GET'])
@authentication
def train_clustering():
    columns = ["id_aspek","nilai_skp","orientasi","integritas","komitmen","disiplin","kerjasama","label"]    
    data = pd.read_sql_table("nilai_aspek_pegawai", con=db.engine, columns=columns)

    data_train = data[columns[1:-1]]
    
    # train dengan kmeans
    kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(data_train)
    centroid = kmeans.cluster_centers_
    # simpan atau update data label data-nya
    for i in range(data_train.shape[0]):
        # data['label'] = kmeans.labels_[i]
        db.engine.execute(f"update nilai_aspek_pegawai set label={kmeans.labels_[i]} where id_aspek={data.iloc[i]['id_aspek']}")
    
    return redirect(url_for('clustering.index'))

@clustering.route('/file-excel', methods=['POST'])
@cross_origin()
def importFile():
    name_col = ['no','nama', 'nilai_skp', 'orientasi', 'integritas', 'komitmen', 'disiplin', 'kerjasama']
    resp = any
    file = request.files['file']
    data = pd.read_excel(file)
    data.columns = name_col
    data_ex = data.to_json(orient="records")
    parsed = json.loads(data_ex)
    resp = jsonify({"message": "success", "data": parsed})
    resp.status_code = 200

    return resp

@clustering.route('/calculate', methods=['POST'])
def prosesPerhitungan():
    response = any
    data = request.get_json() 
    if data['step'] == 'centroid_1':
        data_res = calDistancePoint(centroid[0], data['data'])
        response = jsonify({
            'message': 'success', 
            'informasi': 'Hasil perhitungan jarak tiap feature pada data dengan centroid 1',
            'data':data_res
        })
    
    if data['step'] == 'centroid_2':
        data_res = calDistancePoint(centroid[1], data['data'])
        response = jsonify({
            'message': 'success', 
            'informasi': 'Hasil perhitungan jarak tiap feature pada data dengan centroid 2',
            'data':data_res
        })
    
    if data['step'] == 'distance':
        data_res = calDistanceToCenter(data['data'])
        response = jsonify({
            'message': 'success',
            'informasi': 'Hasil pehitungan jarak antara data dengan centroid cluster',
            'data': data_res   
        })

    return response


def convDfToJson(df):
    data_ex = df.to_json(orient="records")
    return json.loads(data_ex)

def calDistancePoint(cent, data):
    data_pd = pd.json_normalize(data, max_level=1)
    data_pd[col_cal] = cent - data_pd[col_cal] 
    data_ret = convDfToJson(data_pd)
    return data_ret

def calDistanceToCenter(data):
    df = pd.json_normalize(data, max_level=1)
    df['jarak_centroid_0'] = df.apply(lambda r: distance_to_centroid(r, centroid[0]),1)
    df['jarak_centroid_1'] = df.apply(lambda r: distance_to_centroid(r, centroid[1]),1)
    return convDfToJson(df)

def distance_to_centroid(row, centroid):
    row = row[col_cal]
    return euclidean(row, centroid)