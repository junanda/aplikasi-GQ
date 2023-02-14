from flask import render_template, url_for, session, redirect, flash, Blueprint, request
from ..tools import authentication
from ..main import db
from ..model import nilai_aspek, pegawai
import math

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashbord')


# index dashboard
@dashboard.route('/')
@authentication
def index():
    l_active = 'active'
    return render_template('dashboard.html', active_a=l_active)


# list data aspek nilia pegawai
@dashboard.route('/data-aspek/', methods=('POST', 'GET'))
@dashboard.route('/data-aspek/<pg>', methods=('POST', 'GET'))
@dashboard.route('/data-aspek/tahun/<thun>', methods=('POST', 'GET'))
@dashboard.route('/data-aspek/tahun/<thun>/<pg>', methods=('POST', 'GET'))
def alldata(pg=0, thun="all"):
    l_active = 'active'
    dis_able = True

    if thun != 'all':
        query = f"select a.nama_pegawai, b.* from pegawai a inner join nilai_aspek_pegawai b on a.id_pegawai=b.id_pegawai where b.tahun='{thun}' limit 10  offset {str(int(pg)*10)}"
        query2 = f"select a.nama_pegawai, b.* from pegawai a inner join nilai_aspek_pegawai b on a.id_pegawai=b.id_pegawai where b.tahun='{thun}'"
    else:
        query = f"select a.nama_pegawai, b.* from pegawai a inner join nilai_aspek_pegawai b on a.id_pegawai=b.id_pegawai limit 10 offset {str(int(pg)*10)}"
        query2 = f"select a.nama_pegawai, b.* from pegawai a inner join nilai_aspek_pegawai b on a.id_pegawai=b.id_pegawai"
    
    dataPegawai = db.engine.execute(query)
    allRow = db.engine.execute(query2)
    totalPage = math.ceil(len(allRow.fetchall())/10)

    if int(pg) > 0 and int(pg) <= totalPage:
        dis_able = False
    thun = db.session.query(nilai_aspek.NilaiAspekPegawai.tahun).distinct()
    return render_template('data_aspek.html', year=thun, dataAspek=dataPegawai, active_b=l_active, total_page=totalPage, hal=pg, disabled=dis_able)


# view updata data aspek nilai pegawai
@dashboard.route('/data-aspek/edit/<id_data>', methods=('POST', 'GET'))
@authentication
def dataUpdate(id_data):
    data = db.engine.execute(
        'select * from nilai_aspek_pegawai where id_aspek="'+id_data+'"')

    return render_template('view_update.html', data=data)


# proses updata
@dashboard.route('/data-aspek/update-pro/', methods=('POST', 'GET'))
@authentication
def update():
    if request.method == 'POST':
        idapk = request.form['id_aspek']
        skp = request.form['nilai_skp']
        orientasi = request.form['nilai_orientasi']
        integritas = request.form['nilai_integritas']
        komitmen = request.form['nilai_komitmen']
        disiplin = request.form['nilai_disiplin']
        kerjasama = request.form['nilai_kerjasama']

        query = f"update nilai_aspek_pegawai set nilai_skp='{skp}', orientasi='{orientasi}', integritas='{integritas}', komitmen='{komitmen}', disiplin='{disiplin}', kerjasama='{kerjasama}' where id_aspek='{idapk}'"
        db.engine.execute(query)
        return redirect(url_for('dashboard.alldata'))


# delete data pegawai
@dashboard.route('/data-aspek/delete/<idpegawai>', methods=('GET', 'POST'))
@authentication
def deleteData(idpegawai):
    db.engine.execute(
        "delete from nilai_aspek_pegawai where id_aspek='"+idpegawai+"'")
    # dataPegawai = pegawai.Pegawai.query.get(idpegawai)
    # db.session.delete(dataPegawai)
    db.session.commit()
    return redirect(url_for('dashboard.alldata'))


# tambah data training/pegawai
@dashboard.route('/data-aspek/tambah-data', methods=('GET', 'POST'))
@authentication
def newData():
    if request.method == 'POST':
        idPegawai = request.form['id_pegawai']
        nilaiASpek = request.form['nilai_skp']
        orientasi = request.form['nilai_orientasi']
        integritas = request.form['nilai_integritas']
        komitmen = request.form['nilai_komitmen']
        disiplin = request.form['nilai_disiplin']
        kerjasama = request.form['nilai_kerjasama']
        tahun = request.form['tahun']

        data = nilai_aspek.NilaiAspekPegawai(
            id_pegawai=idPegawai,
            nilia_skp=nilaiASpek,
            orientasi=orientasi,
            integritas=integritas,
            komitmen=komitmen,
            disiplin=disiplin,
            kerjasama=kerjasama,
            tahun=tahun
        )

        db.session.add(data)
        db.session.commit()
        flash('record was successfully added')
        return redirect(url_for('dashboard.alldata'))
    dnama = db.engine.execute("select * from pegawai")
    return render_template('view_form_data_aspek.html', data=dnama)
