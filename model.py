from app import db
import datetime


class userstore(db.Model):
    # login password TS
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20))
    password = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer)
    type_of_bed = db.Column(db.String(64))
    date_of_admission = db.Column(
        db.Date, default=datetime.date.today().strftime("%Y-%m-%d"))
    date_of_discharge = db.Column(db.Date)
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    status = db.Column(db.String(64), default='active')
    number_of_days = db.Column(db.Integer)


class MedicineMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(64), index=True)
    quantity = db.Column(db.Integer)
    rate = db.Column(db.Integer)


class Medicines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    medicineID = db.Column(db.Integer, db.ForeignKey(
        'medicine_master.id'), nullable=False)
    patientID = db.Column(db.Integer, db.ForeignKey(
        'patient.id'), nullable=False)


class DiagnosticMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(64), index=True)
    test_charge = db.Column(db.Integer)


class Diagnostics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientID = db.Column(db.Integer, db.ForeignKey(
        'patient.id'), nullable=False)
    testID = db.Column(db.Integer, db.ForeignKey(
        'diagnostic_master.id'), nullable=False)


def init_db():
    db.drop_all()
    db.create_all()
    a = userstore(login='AdmissionEx', password='aaaaaa1@A')
    p = userstore(login='Pharmacist', password='aaaaaa1@A')
    d = userstore(login='DiagnosticEx', password='aaaaaa1@A')
    diag_a = DiagnosticMaster(test_name="ECG", test_charge=1000)
    diag_b = DiagnosticMaster(test_name="CT Scan", test_charge=500)
    diag_c = DiagnosticMaster(test_name="EEG", test_charge=2000)
    db.session.add(diag_a)
    db.session.add(diag_b)
    db.session.add(diag_c)
    db.session.add(a)
    db.session.add(p)
    db.session.add(d)
    db.session.commit()
    db.session.close()
