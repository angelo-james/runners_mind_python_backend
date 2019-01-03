from app import app, mongo
from flask import jsonify

@app.route('/api/users')
def get_all_users():
    users = mongo.db.users
    result = []

    for field in users.find():
      result.append(
        {
          '_id': str(field['_id']),
          'name': field['name']
        }
      )
    return jsonify(result)