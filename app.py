from model import *
from flask import Flask, render_template, request, redirect, flash, url_for
from forms import LoginForm, PatientRegisterForm, PatientSearchForm,patientdetailsForm
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import os
import string
import random
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xee\x1a\x12\xfa|g\xe3K\xdfD9"b~k \xa7]\x15\xa3\xcf\x12\xe2\x9a\x15\x88Z\x12\xb4b$\xa2'
csrf = CSRFProtect()
csrf.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# try:
# except Exception as e:
# print("model : ", e)

# demo database
patient = []
patient_detail = {'ssn': '',
                  'id': '',
                  'name': '',
                  'age': '',
                  'doa': '',
                  'tob': '',
                  'address': '',
                  'state': '',
                  'status': ''}


# Routes


@app.route('/')
@app.route('/home')
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/issuemed')
def home3():
    return render_template('issuemed.html')


@app.route('/diagnostics')
def home1():
    return render_template('diagnostics.html')


@app.route('/finalbill')
def home2():
    return render_template('finalbill.html')


@app.route('/patientdetails', methods=['GET', 'POST'])
def PatientDetails():
  form = patientdetailsForm()
  if request.method == 'POST':
    if form.validate_on_submit():
        flash("Patient Search operation completed", category='info')

  return render_template('patientdetails.html', form = form)



@app.route('/patientdetails/register', methods=['POST', 'GET'])
def PatientRegister():
    def randomString(stringLength=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
    form = PatientRegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient(
                name=form.patient_name.data,
                age=form.patient_age.data,
                date_of_admission=form.date_of_admission.data,
                type_of_bed=form.type_of_bed.data,
                state=form.state.data,
                status=form.status.data,
                city=form.city.data,
                address=form.address.data
            )
            db.session.add(patient)
            db.session.commit()
            db.session.close()
            flash("Patient added successfully", category='success')
            redirect(url_for("PatientRegister"))

    return render_template("patient_register.html", form=form)


@app.route('/patientdetails/search', methods=['POST', 'GET'])
def PatientSearch():
    form = PatientSearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient.query.filter_by(id=form.patient_id.data).first()
            if patient:
                return render_template("patient_search.html", form=form, patient=patient)
            else:
                flash("Patient doesn't exist")
                return render_template("patient_search.html", form=form)
    return render_template("patient_search.html", form=form)


@app.route('/patientdetails/update', methods=['POST', 'GET'])
def PatientUpdate():
    form = PatientRegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient.query.filter_by(
                id=form.patient_id.data).first()
            if patient:
                patient.name = form.patient_name.data,
                patient.age = form.patient_age.data,
                patient.date_of_admission = form.date_of_admission.data,
                patient.type_of_bed = form.type_of_bed.data,
                patient.state = form.state.data,
                patient.status = form.status.data,
                patient.city = form.city.data,
                patient.address = form.address.data
                db.session.commit()
                flash("Patient details updated successfully")
                return redirect(url_for('PatientView'))
            else:
                flash("Patient Doesn't exist")
                return render_template("patient_update.html", form=form)
    return render_template("patient_update.html", form=form)


@app.route('/patientdetails/delete', methods=['POST', 'GET'])
def PatientDelete():
    form = PatientSearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient.query.filter_by(id=form.patient_id.data).first()
            if patient:
<<<<<<< HEAD
                Patient.query.filter_by(id=form.patient_id.data).delete()
                db.session.delete(patient)
                db.session.commit()
                flash("Patient deleted Successfully", category='success')
=======
                try:
                    current_db_session = db.session.object_session(patient)
                    current_db_session.delete(patient)
                    current_db_session.commit()
                    flash("Patient deleted Successfully")
                except Exception:
                    db.session.delete(patient)
>>>>>>> a206c06e9e3565e8ccb44fe00f66e1312e15191b
                return render_template("patient_delete.html", form=form, patient=patient)
            else:
                flash("Patient Doesn't exist")
                return render_template("patient_delete.html", form=form)
    return render_template("patient_delete.html", form=form)


@app.route('/patientdetails/view', methods=['POST', 'GET'])
def PatientView():
    patient = Patient.query.all()
    return render_template("patient_view.html", Patients=patient)


@app.route('/patientdetails/billing', methods=['POST', 'GET'])
def PatientBilling():
    form = PatientSearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient.query.filter_by(id=form.patient_id.data).first()
            if patient:
                number_of_days = (datetime.datetime.now() - patient.date_of_admission).days
                if number_of_days == 0:
                    number_of_days = 1
                db.session.query(Patient).filter_by(
                    id=form.patient_id.data).update({
                        "date_of_discharge": datetime.datetime.now(),
                        "number_of_days": number_of_days,
                        "status": "discharge",
                    })
                if patient.type_of_bed == "general word":
                    total_amount = number_of_days * 2000
                elif patient.type_of_bed == "semi sharing":
                    total_amount = number_of_days * 4000
                elif patient.type_of_bed == "single room":
                    total_amount = number_of_days * 8000
                else:
                    pass
                db.session.commit()
                return render_template("patient_billing.html", form=form, patient=patient, cost=total_amount, days=number_of_days)
            else:
                flash("Patient Doesn't exist")
                return render_template("patient_billing.html", form=form)
    return render_template("patient_billing.html", form=form)


@app.errorhandler(404)
def _404Page(str):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
