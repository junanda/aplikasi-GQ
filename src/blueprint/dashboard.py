from flask import render_template, url_for, session, redirect, flash, Blueprint, request
from ..tools import authentication
from ..main import db
from ..model import nilai_aspek, pegawai

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashbord')


# index dashboard
@dashboard.route('/')
@authentication
def index():
    l_active = 'active'
    return render_template('dashboard.html', active_a=l_active)


# list data pegawai
@dashboard.route('/data-aspek', methods=('POST', 'GET'))
def alldata():
    l_active = 'active'
    dataPegawai = db.engine.execute(
        "select a.nama_pegawai, b.* from pegawai a left join nilai_aspek_pegawai b on a.id_pegawai=b.id_pegawai")
    thun = db.session.query(nilai_aspek.NilaiAspekPegawai.tahun).distinct()

    return render_template('data_aspek.html', year=thun, dataAspek=dataPegawai, active_b=l_active)


# view updata data pegawai
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

        flash(f"data dengan id {id} berhasil di update")
        return redirect(url_for('dashboard.dataUpdate', id_data=idapk))


# delete data pegawai
@dashboard.route('/data-aspek/delete/<idpegawai>', methods=('GET', 'POST'))
@authentication
def deleteData(idpegawai):
    db.engine.execute(
        "delete from nilai_aspek_pegawai where id_pegawai='"+idpegawai+"'")
    dataPegawai = pegawai.Pegawai.query.get(idpegawai)
    db.session.delete(dataPegawai)
    db.session.commit()
    return redirect(url_for('dasboard.alldata'))


# tambah data training/pegawai
@dashboard.route('/tambah-data', methods=('GET', 'POST'))
@authentication
def newData():
    if request.method == 'POST':
        pass
