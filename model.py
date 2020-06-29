from app import db
import datetime


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer)
    type_of_bed = db.Column(db.String(64))
    date_of_admission = db.Column(db.Date, default=datetime.date.today().strftime("%Y-%m-%d"))
    date_of_discharge = db.Column(db.Date)
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    status = db.Column(db.String(64))
    number_of_days = db.Column(db.Integer)


class Medicines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(64), index=True)
    quantity = db.Column(db.Integer)
    

class Diagnostics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(64), index=True)

class MedicineMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(64), index=True)
    quantity = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    



class userstore(db.Model):
    # login password TS
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20))
    password = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    
   
    