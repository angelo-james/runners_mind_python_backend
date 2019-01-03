from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'runners_mind_python'
app.config['MONGO_URI'] = 'mongodb://aj:aj123456@ds052819.mlab.com:52819/runners_mind_python'

db = PyMongo(app)

if __name__ == '__main__':
  app.run(port = 3800, debug=True)