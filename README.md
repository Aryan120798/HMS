# HMS
TCS Case Study 26-June-2020 Hospital Management System.

For execution: ```python app.py ```

# Dependencies
- Flask ```pip install Flask```
- flask_wtf ``` pip install flask_wtf```
- Flask-SQLAlchemy ``` pip install Flask-SQLAlchemy ```
- (Add more dependencies here, as you use in the python file)

## Files for CaseStudy
- [OneDrive link with Edit Access via Browser](https://1drv.ms/u/s!Aua-1wLXX7tLhYZlf6UWp9d8bbkLiQ?e=G6JF5S)

## Assumptions
--Login Button--> Login Page connecting to different dashboards
--Dashboard for Patient with consisits of CRUD links
--Pahmacist Must type exact name of the Medicine

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
a = userstore(login='AdmissionEx', password='aaaaaa1@A')
p = userstore(login='Pharmacist', password='aaaaaa1@A')
d = userstore(login='DiagnosticEx', password='aaaaaa1@A')
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

## 28June
- Aryan
	- HardCode-userstore Table & Values
	- LoginRoute to Dashboards according to the User SignedIn
- Sagar
	- Search Patient
	- Add task to Jira, Add session Management


## ToDo----> subtasks creation and then UI building
- us001-Aryan
- us002-us003-Sagar--Yash
- us004-us005-Tanu--Aryan
- us006-Aryan
- us007-us008-Chiranjeev
- us009-Yash

## UI
- Yash - Template & NavBar

- Aryan - Login-Executive

- Chiranjeev - Dashboard Screen -- Refer: File: "Hospital Management System Case Study 1.0.pdf"
	- Pg-7 5.2.1. Get patient Details Screen
	- Pg-7 5.3.1. Get patient Details Screen
	- Dashboard showing buttons hyperlinked to screens
		- For hyperlinks, see below screens (assigned to tanu)

- Tanu - Single Patient
	- Register
	- Update
	- Delete
	- Search Patient
	- View all Patients

- Sagar
  - Issue Medicine
  - Diagnostic Test
  - Final Patient Billing

hyr
Assumptions:
- Login Button
- Using Dropdowns for redirecting to various pages 
- Dashboard page for the aEx
