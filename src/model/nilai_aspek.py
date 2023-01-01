from main import db
from sqlalchemy import func


class NilaiAspekPegawai(db.Model):
    id_aspek = db.Column(db.Integer, primary_key=True)
    id_pegawai = db.Column(db.Integer, nullable=False)
    nilai_skp = db.Column(db.Float, nullable=False)
    orientasi = db.Column(db.Float, nullable=False)
    integritas = db.Column(db.Float, nullable=False)
    komitmen = db.Column(db.Float, nullable=False)
    disiplin = db.Column(db.Float, nullable=False)
    kerjasama = db.Column(db.Float, nullable=False)
    tahun = db.Column(db.String(4), nullable=False)
    label = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, id_pegawai, nilia_skp, orientasi, integritas, komitmen, disiplin, kerjasama, tahun) -> None:
        super().__init__()
        self.id_pegawai = id_pegawai
        self.nilai_skp = nilia_skp
        self.orientasi = orientasi
        self.integritas = integritas
        self.komitmen = komitmen
        self.disiplin = disiplin
        self.kerjasama = kerjasama
        self.tahun = tahun
