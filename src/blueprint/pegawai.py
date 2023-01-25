from flask import Blueprint, render_template, request, redirect, flash, url_for
from ..tools import authentication
from ..model import pegawai
from ..main import db

bpegawai = Blueprint('pegawai', __name__, url_prefix='/pegawai')

# index pegawai
@bpegawai.route('/', methods=('GET','POST'))
@authentication
def index():
    if request.method == 'POST':
        name = request.form['nama_pegawai']
        newPegawai = pegawai.Pegawai(name=name)
        db.session.add(newPegawai)
        db.session.commit()
        flash('New Pegawai successfuly added')
        return redirect(url_for('pegawai.index'))
    l_active = 'active'
    dataAll = db.engine.execute("select nama_pegawai, id_pegawai from pegawai order by id_pegawai asc")
    return render_template('data_pegawai.html', active_c=l_active, dataPegawai=dataAll)


# edit pegawai
@bpegawai.route('/update/<idpegawai>', methods=('GET','POST'))
@authentication
def updatePegawai(idpegawai):
    if request.method == 'POST':
        idp = request.form['id']
        unama = request.form['nama_pegawai']
        db.engine.execute("update pegawai set nama_pegawai='"+unama+"' where id_pegawai='"+idp+"'")
        flash('Data successully update')
        return redirect(url_for('pegawai.index'))
    dataPegawai = db.engine.execute("select * from pegawai where id_pegawai='"+idpegawai+"'")
    return render_template('form_update_pegawai.html', data=dataPegawai)

# delete pegawai
@bpegawai.route('/delete/<idpegawai>')
@authentication
def delete(idpegawai):
    db.engine.execute("delete from pegawai where id_pegawai='"+idpegawai+"'")
    flash('Delete data successfull')
    return redirect(url_for('pegawai.index'))
