from model import *
from flask import Flask, render_template, request, redirect, flash, url_for
from forms import LoginForm, patientSchema, PatientSearchForm,patientdetailsForm
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import os
import string
import random
from datetime import date

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


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            return render_template('dashboard.html')

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    # this route is for debugging purposes
    # we will access dashboard only after login is successful
    # delete this route before shipping 
    return render_template('dashboard.html')

@app.route('/issuemed')
def issuemed():
    return render_template('issuemed.html')


@app.route('/diagnostics')
def diagnostics():
    return render_template('diagnostics.html')


@app.route('/finalbill')
def finalbill():
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
    form = patientSchema()
    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient(
                ssn=form.patient_ssn.data,
                name=form.patient_name.data,
                age=form.patient_age.data,
                date_of_admission=form.date_of_admission.data,
                type_of_bed=form.type_of_bed.data,
                state=form.state.data,
                status=form.status.data,
                city=form.city.data,
                address=form.address.data
            )
            print(patient.ssn)
            print(type(patient.ssn))
            db.session.add(patient)
            db.session.commit()
            db.session.close()
            flash("Patient added successfully", category='success')
            return redirect(url_for("PatientView"))
        else:
            flash("Validation Failed", category='success')


    return render_template("patient_register.html", form=form)


@app.route('/patientdetails/search', methods=['POST', 'GET'])
def PatientSearch():
    form = PatientSearchForm()
    patientForm = patientSchema()
    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient.query.filter_by(id=form.patient_id.data).first()
            if patient:
                return render_template("patient_search.html", form=form, patientSchema=patientForm, patientData=patient)
            else:
                flash("Patient doesn't exist")
                return render_template("patient_search.html", form=form)
    return render_template("patient_search.html", form=form)


@app.route('/patientdetails/update', methods=['POST', 'GET'])
def PatientUpdate():
    SearchForm = PatientSearchForm()
    patientForm = patientSchema()
    # If Form Submitted
    if request.method == 'POST':
        # Delete Record Requested by User
        if request.form.get('updateRequested') == 'True':
            if patientForm.validate_on_submit():
                patient = Patient.query.filter_by(id=patientForm.patient_id.data).first()
                if patient:
                    # # -------------------Updation Goes Here----------------------
                    patient.name = patientForm.patient_name.data
                    patient.age = patientForm.patient_age.data
                    patient.date_of_admission = patientForm.date_of_admission.data
                    patient.type_of_bed = patientForm.type_of_bed.data
                    patient.state = patientForm.state.data
                    patient.status = patientForm.status.data
                    patient.city = patientForm.city.data
                    patient.address = patientForm.address.data

                    current_db_session = db.session.object_session(patient)
                    current_db_session.commit()
                    db.session.close()
                    flash("Patient Updated Successfully", category='info')

                    return render_template("patient_update.html", SearchForm=SearchForm)
                else:
                    flash("Patient Doesn't exist", category='danger')
                    return render_template("patient_update.html", SearchForm=SearchForm)
        
        # Search Record Requested by User
        if SearchForm.validate_on_submit():
            patient = Patient.query.filter_by(id=SearchForm.patient_id.data).first()
            if patient:
                flash("Patient Found", category='success')
                return render_template("patient_update.html", SearchForm=SearchForm, patientSchema=patientForm, patientData=patient)
            else:
                flash("Patient Doesn't exist", category='danger')
                return render_template("patient_update.html", SearchForm=SearchForm)
        
    return render_template("patient_update.html", SearchForm=SearchForm)


@app.route('/patientdetails/delete', methods=['POST', 'GET'])
def PatientDelete():
    SearchForm = PatientSearchForm()
    patientForm = patientSchema()
    # If Form Submitted
    if request.method == 'POST':
        # Delete Record Requested by User
        if request.form.get('deleteRequested') == 'True':
            if patientForm.validate_on_submit():
                patient = Patient.query.filter_by(id=SearchForm.patient_id.data).first()
                if patient:
                    # # -------------------Deletion Goes Here----------------------
                    current_db_session = db.session.object_session(patient)
                    current_db_session.delete(patient)
                    current_db_session.commit()
                    db.session.close()
                    flash("Patient Deleted Successfully", category='info')

                    return render_template("patient_delete.html", SearchForm=SearchForm)
                else:
                    flash("Patient Doesn't exist", category='danger')
                    return render_template("patient_delete.html", SearchForm=SearchForm)
        
        # Search Record Requested by User
        if SearchForm.validate_on_submit():
            patient = Patient.query.filter_by(id=SearchForm.patient_id.data).first()
            if patient:
                flash("Patient Found", category='success')

                return render_template("patient_delete.html", SearchForm=SearchForm, patientSchema=patientForm, patientData=patient)
            else:
                flash("Patient Doesn't exist", category='danger')
                return render_template("patient_delete.html", SearchForm=SearchForm)
        
    return render_template("patient_delete.html", SearchForm=SearchForm)


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
                number_of_days = (date.today() - patient.date_of_admission).days
                if number_of_days == 0:
                    number_of_days = 1
                db.session.query(Patient).filter_by(
                    id=form.patient_id.data).update({
                        "date_of_discharge": date.today(),
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
                return render_template("patient_billing.html", form=form,cost=total_amount, days=number_of_days)
            else:
                flash("Patient Doesn't exist")
                return render_template("patient_billing.html", form=form)
    return render_template("patient_billing.html", form=form)


@app.errorhandler(404)
def _404Page(str):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
