from model import *
from flask import Flask, render_template, request, redirect, flash, url_for, session
from forms import *
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import os
import string
import random
from datetime import date, datetime


app = Flask(__name__)
app.config[
    'SECRET_KEY'] = os.urandom(32)
csrf = CSRFProtect()
csrf.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Routes
@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('username') == 'AdmissionEx':
        return redirect(url_for('dashboard'))
    elif session.get('username') == 'Pharmacist':
        return redirect(url_for('PharmacyFetch'))
    elif session.get('username') == 'DiagnosticEx':
        return redirect(url_for('DiagnosticsFetch'))
    else:
        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                user = userstore.query.filter_by(login=form.user.data).first()
                if user and user.password == form.password.data:
                    # Log Time Stamp
                    currentTime = datetime.now()
                    user.timestamp = currentTime
                    current_db_session = db.session.object_session(user)
                    current_db_session.commit()
                    _today = currentTime.strftime("%a %d %b %Y")
                    _currentTime = currentTime.strftime("%I:%M %p")
                    db.session.close()
                    if user.login == 'AdmissionEx':
                        session['username'] = user.login
                        flash('Signed in as Admission Executive on {}, at {}'.
                              format(_today, _currentTime),
                              category='info')
                        return redirect(url_for('dashboard'))
                    elif user.login == 'Pharmacist':
                        session['username'] = user.login
                        flash('Signed in as Pharmacist on {}, at {}'.format(
                            _today, _currentTime),
                            category='info')
                        return redirect(url_for('PharmacyFetch'))
                    elif user.login == 'DiagnosticEx':
                        session['username'] = user.login
                        flash('Signed in as Diagnostic Executive on {}, at {}'.
                              format(_today, _currentTime),
                              category='info')
                else:
                    flash('Username or password incorrect', category='danger')
                return redirect(url_for('login'))

        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You are now logged out', 'info')
    return redirect(url_for('login'))


@app.route('/patient/dashboard')
def dashboard():
    # Check if Logged In
    if session.get('username') == 'AdmissionEx':
        return render_template('patient_dashboard.html')
    elif session.get('username') == 'Pharmacist':
        return redirect(url_for('PharmacyFetch'))
    elif session.get('username') == 'DiagnosticEx':
        return redirect(url_for('DiagnosticsFetch'))
    else:
        flash('Kindly Log in First, to continue', category='danger')
        return redirect(url_for('login'))


# ======================= Patient Routes =======================
@app.route('/patientdetails/register', methods=['POST', 'GET'])
def PatientRegister():
    # Check if Logged In
    if session.get('username') == 'AdmissionEx':
        form = patientSchema()
        if request.method == 'POST':
            if form.validate_on_submit():
                if not (form.date_of_admission.data == date.today()):
                    flash("Cannot accept Past or Future dates",
                          category='danger')
                    form.date_of_admission.data = date.today()
                    return render_template("patient_register.html",
                                           form=form,
                                           date=form.date_of_admission.data)
                patient = Patient(
                    ws_ssn=form.patient_ssn.data,
                    ws_pat_name=form.patient_name.data,
                    ws_age=form.patient_age.data,
                    ws_doj=form.date_of_admission.data,
                    ws_rtype=form.type_of_bed.data,
                    ws_state=form.state.data,
                    ws_city=form.city.data,
                    ws_adrs=form.address.data)

                db.session.add(patient)
                db.session.commit()
                db.session.close()
                flash("Patient added successfully", category='success')
                return redirect(url_for("PatientView"))

        return render_template("patient_register.html",
                               form=form,
                               date=form.date_of_admission.data)
    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


# Patient
@app.route('/patientdetails/search', methods=['POST', 'GET'])
def PatientSearch():
    # Check if Logged In
    if session.get('username') == 'AdmissionEx':
        form = PatientSearchForm()
        patientForm = patientSchema()
        if request.method == 'POST':
            if form.validate_on_submit():
                patient = Patient.query.filter_by(ws_pat_id=form.patient_id.data,
                                                  ws_status='active').first()
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

    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


@app.route('/patientdetails/update', methods=['POST', 'GET'])
def PatientUpdate():
    # Check if Logged In
    if session.get('username') == 'AdmissionEx':
        SearchForm = PatientSearchForm()
        patientForm = patientSchema()
        # If Form Submitted
        if request.method == 'POST':
            # Delete Record Requested by User
            if request.form.get('updateRequested') == 'True':
                if patientForm.validate_on_submit():
                    patient = Patient.query.filter_by(
                        ws_pat_id=patientForm.patient_id.data,
                        ws_status='active').first()
                    if patient:
                        # # -------------------Updation Goes Here----------------------
                        patient.ws_pat_name = patientForm.patient_name.data
                        patient.ws_age = patientForm.patient_age.data
                        patient.ws_doj = patientForm.date_of_admission.data
                        patient.ws_rtype = patientForm.type_of_bed.data
                        patient.ws_state = patientForm.state.data
                        patient.ws_city = patientForm.city.data
                        patient.ws_adrs = patientForm.address.data

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
                    ws_pat_id=SearchForm.patient_id.data, ws_status='active').first()
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

    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


@app.route('/patientdetails/delete', methods=['POST', 'GET'])
def PatientDelete():
    # Check if Logged In
    if session.get('username') == 'AdmissionEx':
        SearchForm = PatientSearchForm()
        patientForm = patientSchema()
        # If Form Submitted
        if request.method == 'POST':
            # Delete Record Requested by User
            if request.form.get('deleteRequested') == 'True':
                # if patientForm.validate_on_submit():
                patient = Patient.query.filter_by(
                    ws_pat_id=SearchForm.patient_id.data).first()
                if patient:
                    if patient.ws_status == 'discharge':
                        # # -------------------Deletion Goes Here----------------------
                        patient.ws_status = "deleted"
                        current_db_session = db.session.object_session(patient)
                        current_db_session.commit()
                        db.session.close()
                        flash("Patient Deleted Successfully", category='info')

                        return redirect(url_for("PatientView"))
                    elif patient.ws_status == 'delete':
                        flash(
                            "Patient was already Deleted, You may find its record inside Billing",
                            category='danger')
                        return render_template("patient_delete.html",
                                               SearchForm=SearchForm)
                    else:
                        flash("Patient needs to be Discharged First!",
                              category='danger')
                        return render_template("patient_delete.html",
                                               SearchForm=SearchForm)
                else:
                    flash("Patient Doesn't exist", category='danger')
                    return render_template("patient_delete.html",
                                           SearchForm=SearchForm)

            # Search Record Requested by User
            if SearchForm.validate_on_submit():
                patient = Patient.query.filter_by(
                    ws_pat_id=SearchForm.patient_id.data).first()
                if patient:
                    if patient.ws_status == 'deleted':
                        flash(
                            "Patient was already Deleted, You may find its record inside Billing",
                            category='danger')
                        return render_template("patient_delete.html",
                                               SearchForm=SearchForm)
                    elif patient.ws_status == 'active':
                        flash("Patient needs to be Discharged First!",
                              category='danger')
                        return render_template("patient_delete.html",
                                               SearchForm=SearchForm)
                    else:
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
    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


@app.route('/patientdetails/view', methods=['POST', 'GET'])
def PatientView():
    # Check if Logged In
    if session.get('username') == 'AdmissionEx':
        patient = Patient.query.filter_by(ws_status='active')
        return render_template("patient_view.html", Patients=patient)
    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


@app.route('/patientdetails/billing', methods=['POST', 'GET'])
def PatientBilling():
    # Check if Logged In
    if session.get('username') == 'AdmissionEx':
        form = PatientSearchForm()
        showConfirmBtn = False
        if request.method == 'POST':
            if request.form.get('submit') == 'Search':
                if form.validate_on_submit():
                    patient = Patient.query.filter_by(
                        ws_pat_id=form.patient_id.data).first()
                    if patient:
                        number_of_days = (date.today() -
                                          patient.ws_doj).days
                        if number_of_days == 0:
                            number_of_days = 1
                        if patient.ws_rtype == "General":
                            total_amount = number_of_days * 2000
                        elif patient.ws_rtype == "Semi":
                            total_amount = number_of_days * 4000
                        elif patient.ws_rtype == "Single":
                            total_amount = number_of_days * 8000
                        else:
                            flash('Invalid Room Type', category='danger')
                            return redirect(url_for('PatientView'))
                        flash("Here's your bill, Happy to serve...",
                              category='info')

                        amount = {'medAmount': 0, 'diagAmount': 0}
                        MedJoinedTable = db.session.query(
                            MedicineMaster, Medicines).filter(
                                MedicineMaster.id == Medicines.ws_med_id,
                                Medicines.ws_pat_id == patient.ws_pat_id)
                        db.session.close()
                        if MedJoinedTable:
                            for row in MedJoinedTable:
                                amount['medAmount'] += row[1].ws_qty * row[
                                    0].rate

                        # Search Diagnostics Test Issued History- of Patient.ws_pat_id
                        DiagJoinedTable = db.session.query(
                            DiagnosticMaster, Diagnostics).filter(
                                DiagnosticMaster.id == Diagnostics.ws_diagn,
                                Diagnostics.ws_pat_id == patient.ws_pat_id)
                        db.session.close()
                        if DiagJoinedTable:
                            for row in DiagJoinedTable:
                                amount['diagAmount'] += row[0].test_charge

                        if patient.ws_status == 'active':
                            showConfirmBtn = True

                        return render_template("patient_billing.html",
                                               form=form,
                                               patient=patient,
                                               cost=total_amount,
                                               days=number_of_days,
                                               MedJoinedTable=MedJoinedTable,
                                               DiagJoinedTable=DiagJoinedTable,
                                               amount=amount,
                                               showConfirmBtn=showConfirmBtn)
                    else:
                        flash("Patient Doesn't exist", category='danger')
                        return render_template("patient_billing.html",
                                               form=form)
                # else:
                #     flash("not validated", category='danger')
            if request.form.get('submit') == 'Confirm':
                if form.validate_on_submit():
                    patient = Patient.query.filter_by(ws_pat_id=form.patient_id.data,
                                                      ws_status='active').first()
                    if patient:
                        number_of_days = (date.today() -
                                          patient.ws_doj).days
                        if number_of_days == 0:
                            number_of_days = 1
                        db.session.query(Patient).filter_by(
                            ws_pat_id=patient.ws_pat_id, ws_status='active').update({
                                "ws_dod":
                                date.today(),
                                "ws_nod":
                                number_of_days,
                                "ws_status":
                                "discharge",
                            })
                        db.session.commit()
                        db.session.close()
                        flash('Patient Discharged Successfully',
                              category='success')
                        return redirect(url_for('PatientView'))
                    else:
                        flash("Patient Doesn't exist")
                        return redirect(url_for('PatientBilling'))

        return render_template("patient_billing.html", form=form)
    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


# ======================= Pharmacy Routes =======================
@app.route('/pharmacy/search', methods=['POST', 'GET'])
def PharmacyFetch():
    # Check if Logged In
    if session.get('username') == 'Pharmacist':
        form = PatientSearchForm()
        if request.method == 'POST':
            if request.form.get('submit') == 'Search':
                if form.validate_on_submit():
                    patient = Patient.query.filter_by(ws_pat_id=form.patient_id.data,
                                                      ws_status='active').first()
                    if patient:
                        flash("Patient Found", category='success')

                        # Search Medicine Issued History- of Patient.ws_pat_id
                        MedJoinedTable = db.session.query(
                            MedicineMaster, Medicines).filter(
                                MedicineMaster.id == Medicines.ws_med_id,
                                Medicines.ws_pat_id == patient.ws_pat_id)
                        db.session.close()
                        return render_template("pharmacy_fetch.html",
                                               form=form,
                                               patientData=patient,
                                               MedJoinedTable=MedJoinedTable)
                    else:
                        flash("Patient doesn't exist", category='danger')
                        return render_template("pharmacy_fetch.html",
                                               form=form)
            if request.form.get('submit') == 'Issue Medicines':
                patient = Patient.query.filter_by(ws_pat_id=form.patient_id.data,
                                                  ws_status='active').first()
                return redirect(
                    url_for("PharmacyIssueMed", patientID=str(patient.ws_pat_id)))

        return render_template("pharmacy_fetch.html", form=form)
    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


@app.route('/pharmacy/issuemed', methods=['GET', 'POST'])
def PharmacyIssueMed():
    # Check if Logged In
    if session.get('username') == 'Pharmacist':
        form = IssueMedForm()
        form.med_name.choices = [(i.medicine_name, i.medicine_name)
                                 for i in MedicineMaster.query.all()]
        sessionTable = []
        showAddButton = False
        if request.method == "POST":
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
                        flash("Medicine name: {} Not Found".format(
                            form.med_name.data),
                            category="danger")
                        return render_template(
                            'pharmacy_issuemed.html',
                            form=form,
                            sessionTable=session.get('sessionTable'),
                            medAvailableToAdd=showAddButton)
                # Adding Medicine to Session Table
                if request.form.get('submit') == 'Add Medicine':
                    medicineMasterObj = MedicineMaster.query.filter_by(
                        medicine_name=form.med_name.data).first()
                    if medicineMasterObj:
                        if medicineMasterObj.quantity >= form.med_qty.data:
                            if request.args.get(
                                    'patientID') and Patient.query.filter_by(
                                        ws_pat_id=request.args.get('patientID'),
                                        ws_status='active').first():
                                flash(
                                    "Medicine name: {}, quantity:{} can be purchased-- Stock Available"
                                    .format(form.med_name.data,
                                            form.med_qty.data),
                                    category="success")
                                # Add the Data to Session Table
                                if 'sessionTable' in session:
                                    medID = medicineMasterObj.id
                                    medname = form.med_name.data
                                    qty = int(form.med_qty.data)
                                    rate = int(medicineMasterObj.rate)

                                    sessionTable = session.get('sessionTable')
                                    sessionTable.append(
                                        [medID, medname, qty, rate])
                                    session['sessionTable'] = sessionTable

                                    showAddButton = False
                                    return render_template(
                                        "pharmacy_issuemed.html",
                                        form=form,
                                        sessionTable=session.get(
                                            'sessionTable'),
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
                        flash("Medicine name: {} Not Found".format(
                            form.med_name.data),
                            category="danger")
                        return render_template(
                            "pharmacy_issuemed.html",
                            form=form,
                            sessionTable=session.get('sessionTable'),
                            medAvailableToAdd=showAddButton)
                # Adding Medicine to Session Table
                if request.form.get('submit') == 'Update':
                    # Again Search for the Patient ws_pat_id to be Added
                    if request.args.get(
                            'patientID') and Patient.query.filter_by(
                                ws_pat_id=request.args.get('patientID'),
                                ws_status='active').first():
                        # Initialize SessionTableVar
                        sessionTable = session.get('sessionTable')
                        for medicineTableRecord in sessionTable:
                            # Add the Data to Medicines Table
                            MedicineTableobj = Medicines(
                                ws_qty=medicineTableRecord[2],
                                ws_med_id=medicineTableRecord[0],
                                ws_pat_id=int(request.args.get('patientID')))
                            db.session.add(MedicineTableobj)
                            # Update the Stock in the MedicineMaster Table
                            medicineMasterRecord = MedicineMaster.query.filter_by(
                                id=medicineTableRecord[0]).first()
                            medicineMasterRecord.quantity = medicineMasterRecord.quantity - medicineTableRecord[
                                2]
                            current_db_session = db.session.object_session(
                                medicineMasterRecord)
                            current_db_session.commit()

                        db.session.commit()
                        db.session.close()

                        flash("Medicines Issued Successfully",
                              category='success')
                        return redirect(url_for("PharmacyFetch"))
                    else:
                        flash(
                            'Unable to Find the Patient, Kindly Search Again...',
                            category='danger')
                        return redirect(url_for("PharmacyFetch"))

        # Creating Session Variable
        session['sessionTable'] = sessionTable

        return render_template('pharmacy_issuemed.html',
                               form=form,
                               sessionTable=sessionTable,
                               medAvailableToAdd=showAddButton)

    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


# ======================= Diagnostics Routes =======================
@app.route('/diagnostics/search', methods=['POST', 'GET'])
def DiagnosticsFetch():
    # Check if Logged In
    if session.get('username') == 'DiagnosticEx':
        form = PatientSearchForm()

        if request.method == 'POST':
            if request.form.get('submit') == 'Search':
                if form.validate_on_submit():
                    patient = Patient.query.filter_by(ws_pat_id=form.patient_id.data,
                                                      ws_status='active').first()
                    if patient:
                        flash("Patient Found", category='success')

                        # Search Diagnostics Test Issued History- of Patient.ws_pat_id
                        DiagJoinedTable = db.session.query(
                            DiagnosticMaster, Diagnostics).filter(
                                DiagnosticMaster.id == Diagnostics.ws_diagn,
                                Diagnostics.ws_pat_id == patient.ws_pat_id)
                        db.session.close()
                        return render_template("diagnostics_fetch.html",
                                               form=form,
                                               patientData=patient,
                                               DiagJoinedTable=DiagJoinedTable)
                    else:
                        flash("Patient doesn't exist", category='danger')
                        return render_template("diagnostics_fetch.html",
                                               form=form)
            if request.form.get('submit') == 'Add Test':
                patient = Patient.query.filter_by(ws_pat_id=form.patient_id.data,
                                                  ws_status='active').first()
                return redirect(
                    url_for("DiagnosticsAdd", patientID=str(patient.ws_pat_id)))

        return render_template("diagnostics_fetch.html", form=form)

    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


@app.route('/diagnostics/adddiagnostics', methods=['POST', 'GET'])
def DiagnosticsAdd():
    # Check if Logged In
    if session.get('username') == 'DiagnosticEx':
        form = DiagnosticsForm()
        form.test_name.choices = [(i.test_name, i.test_name)
                                  for i in DiagnosticMaster.query.all()]
        sessionTable = []
        showAddButton = False

        if request.method == "POST":
            if form.validate_on_submit():
                # Checking for Price
                if request.form.get('submit') == 'Check Price':
                    query_data = DiagnosticMaster.query.filter_by(
                        test_name=form.test_name.data).first()
                    showAddButton = True
                    return render_template(
                        "diagnostics_screen.html",
                        form=form,
                        query_data=query_data,
                        sessionTable=session.get('sessionTable'),
                        DiagnosticTestToAdd=showAddButton)
                # Adding Medicine to Session Table
                if request.form.get('submit') == 'Add Test':
                    diagnosticMasterObj = DiagnosticMaster.query.filter_by(
                        test_name=form.test_name.data).first()
                    if diagnosticMasterObj:
                        if request.args.get(
                                'patientID') and Patient.query.filter_by(
                                    ws_pat_id=request.args.get('patientID'),
                                    ws_status='active').first():
                            flash("Test Name: {} can be Issued".format(
                                form.test_name.data),
                                category="success")
                            # Add the Data to Session Table
                            if 'sessionTable' in session:
                                testID = diagnosticMasterObj.id
                                testName = form.test_name.data
                                price = int(diagnosticMasterObj.test_charge)

                                sessionTable = session.get('sessionTable')
                                sessionTable.append([testID, testName, price])
                                session['sessionTable'] = sessionTable

                                showAddButton = False
                                return render_template(
                                    "diagnostics_screen.html",
                                    form=form,
                                    sessionTable=session.get('sessionTable'),
                                    DiagnosticTestToAdd=showAddButton)
                        else:
                            flash(
                                'Unable to Find the Patient, Kindly Search Again...',
                                category='danger')
                            return redirect(url_for("PharmacyFetch"))

                    else:
                        showAddButton = False
                        flash("Diagnostic Test: {} Not Found".format(
                            form.test_name.data),
                            category="danger")
                        return render_template(
                            "diagnostics_screen.html",
                            form=form,
                            sessionTable=session.get('sessionTable'),
                            medAvailableToAdd=showAddButton)
                # Adding Diagnostic Test to Session Table
                if request.form.get('submit') == 'Update':
                    # Again Search for the Patient ws_pat_id to be Added
                    if request.args.get(
                            'patientID') and Patient.query.filter_by(
                                ws_pat_id=request.args.get('patientID'),
                                ws_status='active').first():
                        # Initialize SessionTableVar
                        sessionTable = session.get('sessionTable')
                        for diagnosticTableRecord in sessionTable:
                            # Add the Data to Diagnostic Table
                            DiagnosticTableobj = Diagnostics(
                                ws_pat_id=int(request.args.get('patientID')),
                                ws_diagn=diagnosticTableRecord[0])
                            db.session.add(DiagnosticTableobj)

                        db.session.commit()
                        db.session.close()

                        flash("Test(s) Issued Successfully",
                              category='success')
                        return redirect(url_for("dashboard"))
                    else:
                        flash(
                            'Unable to Find the Patient, Kindly Search Again...',
                            category='danger')
                        return redirect(url_for("DiagnosticFetch"))

        # Creating Session Variable
        session['sessionTable'] = sessionTable


        # diagnostic = DiagnosticMaster.query.all()
        return render_template(
            'diagnostics_screen.html',
            form=form,
            sessionTable=sessionTable,
            medAvailableToAdd=showAddButton,
        )

    else:
        flash('Unauthorised Access', category='danger')
        return redirect(url_for('dashboard'))


@app.errorhandler(404)
def _404Page(str):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
