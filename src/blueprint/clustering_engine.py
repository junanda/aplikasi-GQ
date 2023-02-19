from flask import Blueprint, render_template, redirect, url_for
from ..tools import authentication
from ..main import db
from sklearn.cluster import KMeans
import math
import pandas as pd


clustering = Blueprint('clustering', __name__, url_prefix='/clustering')

#index
@clustering.route('/', methods=('GET','POST'))
@clustering.route('/<pg>', methods=('GET','POST'))
@authentication
def index(pg=0):
    l_active = 'active'
    disabled = True
    # query data cluster dengan pagination
    query = f"select id_aspek, nilai_skp, orientasi, integritas, komitmen, disiplin, kerjasama, label from nilai_aspek_pegawai where label != 'none' limit 20 offset {str(int(pg)*20)}"
    # query untuk mengambil seluruh data nilai_aspek_pegawai
    query2 = "select * from nilai_aspek_pegawai where label !=''"
    dataPag = db.engine.execute(query).fetchall()
    countRow = db.engine.execute(query2).fetchall()
    
    allData = db.engine.execute("select * from nilai_aspek_pegawai").fetchall()

    dataCluster1 = db.engine.execute("select * from nilai_aspek_pegawai where label='0'").fetchall()
    dataCluster2 = len(countRow) - len(dataCluster1)
    data_no_label = len(allData) - len(countRow)
    totalPage = math.ceil(len(countRow)/20)
    if int(pg) > 0 and int(pg) <= totalPage:
        disabled = False
    return render_template(
            'clustering_view.html', 
            active_d=l_active, 
            data_cluster=dataPag, 
            hal=pg, 
            total_page=totalPage, 
            disabled=disabled,
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