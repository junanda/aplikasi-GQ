from flask import Blueprint, render_template, request, redirect, flash, url_for
from ..tools import authentication
from ..model import pegawai
from ..main import db
import math

bpegawai = Blueprint('pegawai', __name__, url_prefix='/pegawai')

# index pegawai
@bpegawai.route('/', methods=('GET','POST'))
@bpegawai.route('/<pg>', methods=('GET', 'POST'))
@authentication
def index(pg=0):
    if request.method == 'POST':
        name = request.form['nama_pegawai']
        newPegawai = pegawai.Pegawai(name=name)
        db.session.add(newPegawai)
        db.session.commit()
        flash('New Pegawai successfuly added')
        return redirect(url_for('pegawai.index'))
    l_active = 'active'
    is_disabled = True
    dataAll = db.engine.execute(f"select nama_pegawai, id_pegawai from pegawai order by id_pegawai asc limit 15 offset {str(int(pg)*15)}")
    allRow = db.engine.execute("select * from pegawai").fetchall()
    totalPage = math.ceil(len(allRow)/15)
    print(totalPage, len(allRow))
    if int(pg) > 0 and int(pg) <= totalPage:
        is_disabled = False
    return render_template('data_pegawai.html', active_c=l_active, dataPegawai=dataAll, hal=pg, total_page=totalPage, disabled=is_disabled)


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
    l_active = 'active'
    dataPegawai = db.engine.execute("select * from pegawai where id_pegawai='"+idpegawai+"'")
    return render_template('form_update_pegawai.html', data=dataPegawai, active_c=l_active)

# delete pegawai
@bpegawai.route('/delete/<idpegawai>')
@authentication
def delete(idpegawai):
    db.engine.execute("delete from nilai_aspek_pegawai where id_pegawai='"+idpegawai+"'")
    db.engine.execute("delete from pegawai where id_pegawai='"+idpegawai+"'")
    flash('Delete data successfull')
    return redirect(url_for('pegawai.index'))
