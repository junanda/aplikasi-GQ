from main import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Object Admin
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(15))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, name, username, password) -> None:
        super().__init__()
        self.name = name
        self.username = username
        self.password = password

    @property
    def is_authenticated(self):
        return super().is_authenticated

    @property
    def is_active(self):
        return super().is_active

    @property
    def get_id(self):
        return self.id
