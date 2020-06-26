from flask import Flask, render_template, request, redirect
from forms import LoginForm
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)

# Routes
@app.route('/')
@app.route('/login')
def login():
  form = LoginForm()
  return render_template('login.html', form = form)

@app.route('/issuemed')
def home3():
  return render_template('issuemed.html')

@app.route('/diagnostics')
def home1():
  return render_template('diagnostics.html')

@app.route('/finalbill')
def home2():
  return render_template('finalbill.html')

@app.route('/patientdetails')
def PatientDetails():
  return render_template('patientdetails.html')

@app.errorhandler(404)
def _404Page(str):
  return render_template('404.html')

if __name__ == '__main__':
  app.run(debug=True)
