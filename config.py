import os

MONGO_DBNAME = os.environ.get('MONGO_DBNAME') or 'runners_mind_python'
MONGO_URI = os.environ.get('MONGODB_URI') or 'mongodb://aj:aj123456@ds052819.mlab.com:52819/runners_mind_python'