from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = PyMongo(app)

if __name__ == '__main__':
  app.run(port=3800, debug=True)