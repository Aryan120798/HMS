from app import db
import datetime


class userstore(db.Model):
    # login password TS
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20))
    password = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Patient(db.Model):
    ws_pat_id = db.Column(db.Integer, primary_key=True)
    ws_ssn = db.Column(db.Integer)
    ws_pat_name = db.Column(db.String(64), index=True)
    ws_age = db.Column(db.Integer)
    ws_rtype = db.Column(db.String(64))
    ws_doj = db.Column(
        db.Date, default=datetime.date.today().strftime("%Y-%m-%d"))
    ws_dod = db.Column(db.Date)
    ws_adrs = db.Column(db.String(64))
    ws_city = db.Column(db.String(64))
    ws_state = db.Column(db.String(64))
    ws_status = db.Column(db.String(64), default='active')
    ws_nod = db.Column(db.Integer)


class MedicineMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(64), index=True)
    quantity = db.Column(db.Integer)
    rate = db.Column(db.Integer)


class Medicines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ws_qty = db.Column(db.Integer)
    ws_med_id = db.Column(db.Integer, db.ForeignKey(
        'medicine_master.id'), nullable=False)
    ws_pat_id = db.Column(db.Integer, db.ForeignKey(
        'patient.ws_pat_id'), nullable=False)


class DiagnosticMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(64), index=True)
    test_charge = db.Column(db.Integer)


class Diagnostics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ws_pat_id = db.Column(db.Integer, db.ForeignKey(
        'patient.ws_pat_id'), nullable=False)
    ws_diagn = db.Column(db.Integer, db.ForeignKey(
        'diagnostic_master.id'), nullable=False)
