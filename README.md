# HMS
TCS Case Study 26-June-2020 Hospital Management System.

***
FOR Submission code, refer Branch: submitted-code
***
Create Virtual Environment first (ignore if created)
	For installing all dependencies: ```python -m venv venv```
	
Then execute the below commands

For installing all dependencies: ```pip install -r requirements.txt ```
For execution: ```python app.py ```

# Dependencies
- Flask ```pip install Flask```
- flask_wtf ``` pip install flask_wtf```
- wtform-Email-Validator ``` pip install wtforms[email]```
- Flask-SQLAlchemy ``` pip install Flask-SQLAlchemy ```

## Files for CaseStudy
https://drive.google.com/drive/folders/1brNKXbyE31YCQ7ZIgoUzOJAgjk53YwHx?usp=sharing

## Login Details
  - <UserType> Admission Executive
  	- UserName: AdmissionEx
  	- Password: 123qwe!@QW
  - <UserType> Pharmacist
  	- UserName: Pharmacist
  	- Password: 123qwe!@QW
  - <UserType> Diagnostic Executive
  	- UserName: DiagnosticEx
  	- Password: 123qwe!@QW

## Assumptions
--Login Button--> Login Page connecting to different dashboards
--Dashboard for Patient with consisits of CRUD links
--Pahmacist Must type exact name of the Medicine
--Patient billins used for searching history of all the patients irrespective of its stauts for recorde purpose.

## Issue Med UI
- Flag Var for AddBtn
- para, 2--CheckAvailability--->
	- if Yes, Available--->
		- Flash: MedAvailable
		- Show AddBtn
			- if User clicks on AddBtn
				- Check Availability
				- then Add data to DB-MedTable
				- Reload the Page with Medadded FlashMsg
				- Hide AddBtn
				- Populate the UI-MedTable from the TMP Table in DataBase
	- else
		- Reload the Page with Unavailable FlashMsg but keep the State of Table as it is

## Python Shell Commands
```
from model import *
db.session.close()
db.drop_all()
db.create_all()
a = userstore(login='AdmissionEx', password='123qwe!@QW')
p = userstore(login='Pharmacist', password='123qwe!@QW')
d = userstore(login='DiagnosticEx', password='123qwe!@QW')
db.session.add(a)
db.session.add(p)
db.session.add(d)
db.session.commit()
db.session.close()

##### Tabler Data Update- for MedicineMaster Table for Quantity Update
from model import *
m = MedicineMaster.query.filter_by(medicine_name= '<StringValueHere>' ).first()
m.quantity = <ValueHere>
db.session.add(m)
db.session.commit()
db.session.close()
```
