from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.from_pyfile('config.py')

mongo = PyMongo(app)

app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

from routes.user import *
from routes.post import *
from routes.comment import *
from routes.postCoords import *

if __name__ == '__main__':
  app.run(port=3800, debug=True)