from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_pyfile('config.py')

mongo = PyMongo(app)

from routes.user import *
from routes.post import *
from routes.comment import *

if __name__ == '__main__':
  app.run(port=3800, debug=True)