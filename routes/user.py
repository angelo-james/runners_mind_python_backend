from app import app, mongo
from flask_restful import Resource, Api
from flask import jsonify, request
from bson.objectid import ObjectId

api = Api(app)

class GetAllUsers(Resource):
  def get(self):
    users = mongo.db.users
    data = []

    for field in users.find():
      data.append(
        {
          '_id': str(field['_id']),
          'username': field['name']
        }
      )
    return jsonify(data)

class AddUser(Resource):
  def post(self):
    users = mongo.db.users
    name = request.get_json()['name']

    name_id = users.insert(
      {
        'name': name
      }
    )

    new_user = users.find_one({'_id': name_id})

    result = {'username': new_user['name'], 'message': 'user was created successfully'}

    return jsonify({'data': result})

class UpdateUser(Resource):
  def put(self, id):
    users = mongo.db.users
    name = request.get_json()['name']

    users.find_one_and_update({'_id': ObjectId(id)}, {'$set': {'name': name}}, upsert=False)
    new_user = users.find_one({'_id': ObjectId(id)})

    result = {'username': new_user['name'], 'message': 'user was updated successfully'}

    return jsonify({'data': result})

class DeleteUser(Resource):
  def delete(self, id):
    users = mongo.db.users

    response = users.delete_one({'_id': ObjectId(id)})

    if response.deleted_count == 1:
      result = {'message': 'user deleted successfully'}
    else:
      result = {'message': 'failed to delete user'}

    return jsonify({'data': result})

api.add_resource(GetAllUsers, '/api/users')
api.add_resource(AddUser, '/api/users')
api.add_resource(UpdateUser, '/api/users/<id>')
api.add_resource(DeleteUser, '/api/users/<id>')
