from flask import render_template, url_for, session, redirect, flash, Blueprint, request
from ..tools import authentication
from ..main import db


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashbord')


# index dashboard
@dashboard.route('/')
@authentication
def index():
    return render_template('dashboard.html')


# list data pegawai
@dashboard.route('/data-aspek', methods=('POST', 'GET'))
def alldata():
    return render_template('data_aspek.html')

# updata data pegawai


@dashboard.route('/update/<int:id_data>', methods=('POST', 'GET'))
def dataUpdate(id_data):
    data = db.engine.execute(
        'select a.nama_pegawai, b.id_aspek, b.nilai_skp, b. from ')
    pass
# proses updata
# delete data pegawai
# tambah data training/pegawai
