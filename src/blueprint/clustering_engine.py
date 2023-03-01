from flask import Blueprint, render_template, redirect, url_for, request, json, jsonify
from flask_cors import cross_origin
from fileinput import filename
from ..tools import authentication
from ..main import db
from sklearn.cluster import KMeans
import math
import pandas as pd


clustering = Blueprint('clustering', __name__, url_prefix='/clustering')

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
    resp = any
    file = request.files['file']
    data = pd.read_excel(file)
    data_ex = data.to_json(orient="records")
    parsed = json.loads(data_ex)
    print(parsed[1:])
    resp = jsonify({"message": "success", "data": parsed})
    resp.status_code = 200

    return resp
