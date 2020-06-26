from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Routes
@app.route('/')
def home():
  return render_template('home.html')

@app.errorhandler(404)
def _404Page(str):
  return render_template('404.html')

if __name__ == '__main__':
  app.run(debug=True)