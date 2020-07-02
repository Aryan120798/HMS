from app import db
from dbData import db_dict
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
    for tablename, values in db_dict.items():
        for row in values:
            if tablename == "userstore":
                user = userstore(login=row['login'], password=row['password'])
                db.session.add(user)
            elif tablename == "DiagnosticMaster":
                diag_name = DiagnosticMaster(
                    test_name=row['test_name'], test_charge=row['test_charge'])
                db.session.add(diag_name)
            elif tablename == "MedicineMaster":
                medicine = MedicineMaster(
                    medicine_name=row['medicine_name'],
                    quantity=row['quantity'],
                    rate=row['rate']
                )
                db.session.add(medicine)
            db.session.commit()
    db.session.close()
