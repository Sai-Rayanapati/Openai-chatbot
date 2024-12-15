from datetime import datetime
from . import db


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    messagetype = db.Column(db.String(100))
    message = db.Column(db.String(500))
