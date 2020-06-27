from app import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer)
    type_of_bed = db.Column(db.String(64))
    date_of_admission = db.Column(db.DateTime)
    date_of_discharge = db.Column(db.DateTime)
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    status = db.Column(db.String(64))
    number_of_days = db.Column(db.Integer)