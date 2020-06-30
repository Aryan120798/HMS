from model import *
from flask import Flask, render_template, request, redirect, flash, url_for, session
from forms import *
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import os
import string
import random
from datetime import date

app = Flask(__name__)
app.config[
    'SECRET_KEY'] = b'\xee\x1a\x12\xfa|g\xe3K\xdfD9"b~k \xa7]\x15\xa3\xcf\x12\xe2\x9a\x15\x88Z\x12\xb4b$\xa2'
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
patient_detail = {
    'ssn': '',
    'id': '',
    'name': '',
    'age': '',
    'doa': '',
    'tob': '',
    'address': '',
    'state': '',
    'status': ''
}


# Routes
@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.user.data)
            user = userstore.query.filter_by(login=form.user.data).first()
            user_pass = userstore.query.filter_by(
                password=form.password.data).first()
            if user and user_pass:
                patient_fetch_form = PatientSearchForm()
                pharmacy_fetch_from = PatientSearchForm()
                if user.login == 'AdmissionEx':
                    session['username'] = user.login
                    flash('Signed in as Admission Executive',
                          category='success')
                    return redirect(url_for('PatientDashboard'))
                elif user.login == 'Pharmacist':
                    session['username'] = user.login
                    flash('Signed in as Pharmacist',
                          category='success')
                    return redirect(url_for('PharmacyFetch'))
                elif user.login == 'DiagnosticEx':
                    session['username'] = user.login
                    flash('Signed in as Diagnostic Executive',
                          category='success')
                    return redirect(url_for('DiagnosticsFetch'))
                else:
                    flash('Username or password incorrect', category='danger')
            else:
                flash('Username or password incorrect', category='danger')
        #return render_template('dashboard.html')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You are now logged out', 'info')
    return redirect(url_for('login'))


# ======================= Patient Routes =======================


@app.route('/patient/dashboard')
def PatientDashboard():
    return render_template('dashboard.html')


@app.route('/patientdetails/register', methods=['POST', 'GET'])
def PatientRegister():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    form = patientSchema()
    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient(ssn=form.patient_ssn.data,
                              name=form.patient_name.data,
                              age=form.patient_age.data,
                              date_of_admission=form.date_of_admission.data,
                              type_of_bed=form.type_of_bed.data,
                              state=form.state.data,
                              status=form.status.data,
                              city=form.city.data,
                              address=form.address.data)
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


# Patient
@app.route('/patientdetails/search', methods=['POST', 'GET'])
def PatientSearch():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    form = PatientSearchForm()
    patientForm = patientSchema()
    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient.query.filter_by(id=form.patient_id.data).first()
            if patient:
                flash("Patient Found", category='success')
                return render_template("patient_search.html",
                                       form=form,
                                       patientSchema=patientForm,
                                       patientData=patient)
            else:
                flash("Patient doesn't exist", category='danger')
                return render_template("patient_search.html", form=form)
    return render_template("patient_search.html", form=form)


@app.route('/patientdetails/update', methods=['POST', 'GET'])
def PatientUpdate():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    SearchForm = PatientSearchForm()
    patientForm = patientSchema()
    # If Form Submitted
    if request.method == 'POST':
        # Delete Record Requested by User
        if request.form.get('updateRequested') == 'True':
            if patientForm.validate_on_submit():
                patient = Patient.query.filter_by(
                    id=patientForm.patient_id.data).first()
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

                    return redirect(url_for('PatientView'))
                    # return render_template("patient_update.html", SearchForm=SearchForm)
                else:
                    flash("Patient Doesn't exist", category='danger')
                    return render_template("patient_update.html",
                                           SearchForm=SearchForm)

        # Search Record Requested by User
        if SearchForm.validate_on_submit():
            patient = Patient.query.filter_by(
                id=SearchForm.patient_id.data).first()
            if patient:
                flash("Patient Found", category='success')
                return render_template("patient_update.html",
                                       SearchForm=SearchForm,
                                       patientSchema=patientForm,
                                       patientData=patient)
            else:
                flash("Patient Doesn't exist", category='danger')
                return render_template("patient_update.html",
                                       SearchForm=SearchForm)

    return render_template("patient_update.html", SearchForm=SearchForm)


@app.route('/patientdetails/delete', methods=['POST', 'GET'])
def PatientDelete():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    SearchForm = PatientSearchForm()
    patientForm = patientSchema()
    # If Form Submitted
    if request.method == 'POST':
        # Delete Record Requested by User
        if request.form.get('deleteRequested') == 'True':
            if patientForm.validate_on_submit():
                patient = Patient.query.filter_by(
                    id=SearchForm.patient_id.data).first()
                if patient:
                    # # -------------------Deletion Goes Here----------------------
                    current_db_session = db.session.object_session(patient)
                    current_db_session.delete(patient)
                    current_db_session.commit()
                    db.session.close()
                    flash("Patient Deleted Successfully", category='info')

                    return render_template("patient_delete.html",
                                           SearchForm=SearchForm)
                else:
                    flash("Patient Doesn't exist", category='danger')
                    return render_template("patient_delete.html",
                                           SearchForm=SearchForm)

        # Search Record Requested by User
        if SearchForm.validate_on_submit():
            patient = Patient.query.filter_by(
                id=SearchForm.patient_id.data).first()
            if patient:
                flash("Patient Found", category='success')

                return render_template("patient_delete.html",
                                       SearchForm=SearchForm,
                                       patientSchema=patientForm,
                                       patientData=patient)
            else:
                flash("Patient Doesn't exist", category='danger')
                return render_template("patient_delete.html",
                                       SearchForm=SearchForm)

    return render_template("patient_delete.html", SearchForm=SearchForm)


@app.route('/patientdetails/view', methods=['POST', 'GET'])
def PatientView():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    patient = Patient.query.all()
    return render_template("patient_view.html", Patients=patient)


@app.route('/patientdetails/billing', methods=['POST', 'GET'])
def PatientBilling():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    form = PatientSearchForm()
    if request.method == 'POST':
        print('Insisde POST')
        if form.validate_on_submit():
            print('Validation Successful')
            patient = Patient.query.filter_by(id=form.patient_id.data).first()
            if patient:
                number_of_days = (date.today() -
                                  patient.date_of_admission).days
                if number_of_days == 0:
                    number_of_days = 1
                db.session.query(Patient).filter_by(
                    id=form.patient_id.data).update({
                        "date_of_discharge":
                        date.today(),
                        "number_of_days":
                        number_of_days,
                        "status":
                        "discharge",
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
                print('Data Commited')
                flash("Here's your bill, Happy to serve...", category='info')
                return render_template("patient_billing.html",
                                       form=form,
                                       patient=patient,
                                       cost=total_amount,
                                       days=number_of_days)
            else:
                flash("Patient Doesn't exist")
                return render_template("patient_billing.html", form=form)
        else:
            flash("Validation Unsuccessful")
            print('Validation Unsuccessful')
    return render_template("patient_billing.html", form=form)


# ======================= Pharmacy Routes =======================
@app.route('/pharmacy/fetch', methods=['POST', 'GET'])
def PharmacyFetch():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    form = PatientSearchForm()
    if request.method == 'POST':
        if request.form.get('submit') == 'Fetch':
            if form.validate_on_submit():
                patient = Patient.query.filter_by(
                    id=form.patient_id.data).first()
                if patient:
                    flash("Patient Found", category='success')

                    # Fetch Medicine Issued History- of Patient.id
                    MedJoinedTable = db.session.query(MedicineMaster, Medicines).filter(MedicineMaster.id==Medicines.medicineID, Medicines.patientID == patient.id)
                    db.session.close()
                    
                    return render_template("pharmacy_fetch.html",
                                           form=form,
                                           patientData=patient, MedJoinedTable=MedJoinedTable)
                else:
                    flash("Patient doesn't exist", category='danger')
                    return render_template("pharmacy_fetch.html", form=form)
        if request.form.get('submit') == 'Issue Medicines':
            patient = Patient.query.filter_by(id=form.patient_id.data).first()
            return redirect(
                url_for("PharmacyIssueMed", patientID=str(patient.id)))

    return render_template("pharmacy_fetch.html", form=form)


@app.route('/pharmacy/issuemed', methods=['GET', 'POST'])
def PharmacyIssueMed():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    form = IssueMedForm()
    sessionTable = []
    showAddButton = False
    if form.validate_on_submit():
        # Checking for Availability
        if request.form.get('submit') == 'Check Availability':
            medicineMasterObj = MedicineMaster.query.filter_by(
                medicine_name=form.med_name.data).first()
            if medicineMasterObj:
                if medicineMasterObj.quantity >= form.med_qty.data:
                    showAddButton = True
                    flash(
                        "Medicine name: {}, quantity:{} can be purchased-- Stock Available"
                        .format(form.med_name.data, form.med_qty.data),
                        category="success")
                    return render_template(
                        'pharmacy_issuemed.html',
                        form=form,
                        sessionTable=session.get('sessionTable'),
                        medAvailableToAdd=showAddButton)
                else:
                    flash(
                        "Medicine name: {}, quantity:{} can't be purchased-- as Only {} pcs Available"
                        .format(form.med_name.data, form.med_qty.data,
                                medicineMasterObj.quantity),
                        category="danger")
                    return render_template(
                        'pharmacy_issuemed.html',
                        form=form,
                        sessionTable=session.get('sessionTable'),
                        medAvailableToAdd=showAddButton)
            else:
                flash("Medicine name: {} Not Found".format(form.med_name.data),
                      category="danger")
                return render_template(
                    'pharmacy_issuemed.html',
                    form=form,
                    sessionTable=session.get('sessionTable'),
                    medAvailableToAdd=showAddButton)
        # Adding Medicine to Session Table
        if request.form.get('submit') == 'Add Medicine':
            print('=======Addition Performed Successfully=======')
            medicineMasterObj = MedicineMaster.query.filter_by(
                medicine_name=form.med_name.data).first()
            if medicineMasterObj:
                if medicineMasterObj.quantity >= form.med_qty.data:
                    if request.args.get(
                            'patientID') and Patient.query.filter_by(
                                id=request.args.get('patientID')).first():
                        print(request.args.get('patientID'))
                        flash(
                            "Medicine name: {}, quantity:{} can be purchased-- Stock Available"
                            .format(form.med_name.data, form.med_qty.data),
                            category="success")
                        # Add the Data to Session Table
                        if 'sessionTable' in session:
                            print('session present')
                            medID = medicineMasterObj.id
                            medname = form.med_name.data
                            qty = int(form.med_qty.data)
                            rate = int(medicineMasterObj.rate)

                            sessionTable = session.get('sessionTable')
                            sessionTable.append([medID, medname, qty, rate])
                            session['sessionTable'] = sessionTable
                            print(sessionTable)
                            print(session.get('sessionTable'))

                            showAddButton = False
                            return render_template(
                                "pharmacy_issuemed.html",
                                form=form,
                                sessionTable=session.get('sessionTable'),
                                medAvailableToAdd=showAddButton)
                    else:
                        flash(
                            'Unable to Find the Patient, Kindly Search Again...',
                            category='danger')
                        return redirect(url_for("PharmacyFetch"))
                else:
                    showAddButton = False
                    flash(
                        "Medicine name: {}, quantity:{} can't be purchased-- as Only {} pcs Available"
                        .format(form.med_name.data, form.med_qty.data,
                                medicineMasterObj.quantity),
                        category="danger")
                    return render_template(
                        "pharmacy_issuemed.html",
                        form=form,
                        sessionTable=session.get('sessionTable'),
                        medAvailableToAdd=showAddButton)
            else:
                showAddButton = False
                flash("Medicine name: {} Not Found".format(form.med_name.data),
                      category="danger")
                return render_template(
                    "pharmacy_issuemed.html",
                    form=form,
                    sessionTable=session.get('sessionTable'),
                    medAvailableToAdd=showAddButton)
        # Adding Medicine to Session Table
        if request.form.get('submit') == 'Update':
            print('=======Issue Medicine Performed Successfully=======')
            # Again Search for the Patient ID to be Added
            if request.args.get('patientID') and Patient.query.filter_by(
                    id=request.args.get('patientID')).first():
                # Initialize SessionTableVar
                sessionTable = session.get('sessionTable')
                for medicineTableRecord in sessionTable:
                    # Add the Data to Medicines Table
                    MedicineTableobj = Medicines(
                        quantity=medicineTableRecord[2],
                        medicineID=medicineTableRecord[0],
                        patientID=int(request.args.get('patientID')))
                    db.session.add(MedicineTableobj)
                    # Update the Stock in the MedicineMaster Table
                    medicineMasterRecord = MedicineMaster.query.filter_by(id=medicineTableRecord[0]).first()
                    medicineMasterRecord.quantity = medicineMasterRecord.quantity - medicineTableRecord[2]
                    current_db_session = db.session.object_session(medicineMasterRecord)
                    current_db_session.commit()

                db.session.commit()
                db.session.close()

                flash("Medicines Issued Successfully", category='success')
                return redirect(url_for("PharmacyFetch"))
            else:
                flash('Unable to Find the Patient, Kindly Search Again...',
                      category='danger')
                return redirect(url_for("PharmacyFetch"))

    # Creating Session Variable
    print('session NOT present')
    session['sessionTable'] = sessionTable
    print('Seession Created======')

    print(session.get('sessionTable'))
    return render_template('pharmacy_issuemed.html',
                           form=form,
                           sessionTable=sessionTable,
                           medAvailableToAdd=showAddButton)


# ======================= Diagnostics Routes =======================
@app.route('/diagnostics/fetch', methods=['POST', 'GET'])
def DiagnosticsFetch():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    form = PatientSearchForm()
    
    if request.method == 'POST':
        if request.form.get('submit') == 'Fetch':
            if form.validate_on_submit():
                patient = Patient.query.filter_by(
                    id=form.patient_id.data).first()
                if patient:
                    flash("Patient Found", category='success')

                    # Fetch Medicine Issued History- of Patient.id
                    # MedJoinedTable = db.session.query(MedicineMaster, Medicines).filter(MedicineMaster.id==Medicines.medicineID, Medicines.patientID == patient.id)
                    # db.session.close()
                    
                    return render_template("diagnostics_fetch.html",
                                           form=form,
                                           patientData=patient)
                else:
                    flash("Patient doesn't exist", category='danger')
                    return render_template("diagnostics_fetch.html", form=form)
        if request.form.get('submit') == 'Add Diagnostics':
            patient = Patient.query.filter_by(id=form.patient_id.data).first()
            return redirect(url_for("DiagnosticsAdd", patientID=str(patient.id)))

    
    return render_template("diagnostics_fetch.html", form=form)


@app.route('/diagnostics/adddiagnostics')
def DiagnosticsAdd():
    # Check if Logged In
    if session.get('username') == None:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))

    form = DiagnosticsForm()
    sessionTable = []
    showAddButton = False
    if form.validate_on_submit():
        # Checking for Availability
        if request.form.get('submit') == 'Check Availability':
            medicineMasterObj = MedicineMaster.query.filter_by(
                medicine_name=form.med_name.data).first()
            if medicineMasterObj:
                if medicineMasterObj.quantity >= form.med_qty.data:
                    showAddButton = True
                    flash(
                        "Medicine name: {}, quantity:{} can be purchased-- Stock Available"
                        .format(form.med_name.data, form.med_qty.data),
                        category="success")
                    return render_template(
                        'pharmacy_issuemed.html',
                        form=form,
                        sessionTable=session.get('sessionTable'),
                        medAvailableToAdd=showAddButton)
                else:
                    flash(
                        "Medicine name: {}, quantity:{} can't be purchased-- as Only {} pcs Available"
                        .format(form.med_name.data, form.med_qty.data,
                                medicineMasterObj.quantity),
                        category="danger")
                    return render_template(
                        'pharmacy_issuemed.html',
                        form=form,
                        sessionTable=session.get('sessionTable'),
                        medAvailableToAdd=showAddButton)
            else:
                flash("Medicine name: {} Not Found".format(form.med_name.data),
                      category="danger")
                return render_template(
                    'pharmacy_issuemed.html',
                    form=form,
                    sessionTable=session.get('sessionTable'),
                    medAvailableToAdd=showAddButton)
        # Adding Medicine to Session Table
        if request.form.get('submit') == 'Add Medicine':
            print('=======Addition Performed Successfully=======')
            medicineMasterObj = MedicineMaster.query.filter_by(
                medicine_name=form.med_name.data).first()
            if medicineMasterObj:
                if medicineMasterObj.quantity >= form.med_qty.data:
                    if request.args.get(
                            'patientID') and Patient.query.filter_by(
                                id=request.args.get('patientID')).first():
                        print(request.args.get('patientID'))
                        flash(
                            "Medicine name: {}, quantity:{} can be purchased-- Stock Available"
                            .format(form.med_name.data, form.med_qty.data),
                            category="success")
                        # Add the Data to Session Table
                        if 'sessionTable' in session:
                            print('session present')
                            medID = medicineMasterObj.id
                            medname = form.med_name.data
                            qty = int(form.med_qty.data)
                            rate = int(medicineMasterObj.rate)

                            sessionTable = session.get('sessionTable')
                            sessionTable.append([medID, medname, qty, rate])
                            session['sessionTable'] = sessionTable
                            print(sessionTable)
                            print(session.get('sessionTable'))

                            showAddButton = False
                            return render_template(
                                "pharmacy_issuemed.html",
                                form=form,
                                sessionTable=session.get('sessionTable'),
                                medAvailableToAdd=showAddButton)
                    else:
                        flash(
                            'Unable to Find the Patient, Kindly Search Again...',
                            category='danger')
                        return redirect(url_for("PharmacyFetch"))
                else:
                    showAddButton = False
                    flash(
                        "Medicine name: {}, quantity:{} can't be purchased-- as Only {} pcs Available"
                        .format(form.med_name.data, form.med_qty.data,
                                medicineMasterObj.quantity),
                        category="danger")
                    return render_template(
                        "pharmacy_issuemed.html",
                        form=form,
                        sessionTable=session.get('sessionTable'),
                        medAvailableToAdd=showAddButton)
            else:
                showAddButton = False
                flash("Medicine name: {} Not Found".format(form.med_name.data),
                      category="danger")
                return render_template(
                    "pharmacy_issuemed.html",
                    form=form,
                    sessionTable=session.get('sessionTable'),
                    medAvailableToAdd=showAddButton)
        # Adding Medicine to Session Table
        if request.form.get('submit') == 'Update':
            print('=======Issue Medicine Performed Successfully=======')
            # Again Search for the Patient ID to be Added
            if request.args.get('patientID') and Patient.query.filter_by(
                    id=request.args.get('patientID')).first():
                # Initialize SessionTableVar
                sessionTable = session.get('sessionTable')
                for medicineTableRecord in sessionTable:
                    # Add the Data to Medicines Table
                    MedicineTableobj = Medicines(
                        quantity=medicineTableRecord[2],
                        medicineID=medicineTableRecord[0],
                        patientID=int(request.args.get('patientID')))
                    db.session.add(MedicineTableobj)
                    # Update the Stock in the MedicineMaster Table
                    medicineMasterRecord = MedicineMaster.query.filter_by(id=medicineTableRecord[0]).first()
                    medicineMasterRecord.quantity = medicineMasterRecord.quantity - medicineTableRecord[2]
                    current_db_session = db.session.object_session(medicineMasterRecord)
                    current_db_session.commit()

                db.session.commit()
                db.session.close()

                flash("Medicines Issued Successfully", category='success')
                return redirect(url_for("PharmacyFetch"))
            else:
                flash('Unable to Find the Patient, Kindly Search Again...',
                      category='danger')
                return redirect(url_for("PharmacyFetch"))

    # Creating Session Variable
    print('session NOT present')
    session['sessionTable'] = sessionTable
    print('Seession Created======')

    print(session.get('sessionTable'))

    diagnostic = DiagnosticMaster.query.all()
    return render_template('diagnostics_screen.html',
                           form=form,
                           sessionTable=sessionTable,
                           medAvailableToAdd=showAddButton, diagnosticMS=diagnostic)



@app.errorhandler(404)
def _404Page(str):
    return render_template('404.html')


@app.route('/tmp', methods=['GET', 'POST'])
def tmp():
    medicineTable = []
    # medicineTable = [
    #     [1,'para',10,20],
    #     [2,'crocin',10,20],
    #     [3,'betadine',10,20],
    #     [4,'para',10,20]
    # ]

    if 'tmpTable' in session:
        if request.method == 'POST':
            print('session present')
            medname = request.form.get('medname')
            qty = int(request.form.get('qty'))
            rate = int(request.form.get('rate'))

            medicineTable = session.get('tmpTable')
            medicineTable.append([medname, qty, rate])
            session['tmpTable'] = medicineTable
            print(medicineTable)
            print(session.get('tmpTable'))

            return render_template('tmp.html',
                                   medicineTable=session.get('tmpTable'))

    print('session NOT present')
    session['tmpTable'] = medicineTable
    print('Seession Created======')

    print(session.get('tmpTable'))

    return render_template('tmp.html')


@app.route('/delete')
def delete_visits():
    session.pop('tmpTable', None)
    print('Seession Cleared...')
    # return redirect(url_for('tmp'))
    return redirect(url_for('PharmacyIssueMed'))


if __name__ == '__main__':
    app.run(debug=True)
