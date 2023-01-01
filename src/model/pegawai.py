from ..main import db
from sqlalchemy.sql import func


class Pegawai(db.Model):
    id_pegawai = db.Column(db.Integer, primary_key=True)
    nama_pegawai = db.Column(db.String(15))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, name) -> None:
        super().__init__()
        self.nama_pegawai = name

    def __repr__(self) -> str:
        return "%r" % (self.nama_pegawai)
