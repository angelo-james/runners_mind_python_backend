from app import app, mongo
from flask_restful import Resource, Api
from flask import jsonify, request
from bson.objectid import ObjectId
import bcrypt, datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)

api = Api(app)

class GetAllUsers(Resource):
  def get(self):
    users = mongo.db.users
    data = []

    for field in users.find():
      data.append(
        {
          '_id': str(field['_id']),
          'username': field['name'],
          'email': field['email'],
          'password': field['password'],
          'followers': field['followers'],
          'following': field['following']
        }
      )
    return jsonify(data)

class Login(Resource):
  def post(self):
    users = mongo.db.users
    email = request.get_json()['email']
    password = request.get_json()['password']
    
    user = users.find_one({
      'email': email
    })
    user['_id'] = str(user['_id'])
    
    if user and bcrypt.checkpw(password.encode('utf8'), user['password'].encode('utf8')):

      token = create_access_token(identity=user['_id'], fresh=True, expires_delta=datetime.timedelta(days=1), )

      user['token'] = token
      user.pop('password', 0)
      
      return jsonify(user)



class AddUser(Resource):
  def post(self):
    users = mongo.db.users
    name = request.get_json()['name']
    email = request.get_json()['email']
    password = request.get_json()['password']
    hashPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10))

    name_id = users.insert(
      {
        'name': name,
        'email': email,
        'password': hashPassword.decode('utf8'),
        'followers': [],
        'following': [],
        'posts': []
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

class Follow(Resource):
  def put(self, id):
    users = mongo.db.users
    userId = request.get_json()['userId']

    user = users.find_one_and_update({'_id': ObjectId(id)}, {'$addToSet': {'followers': userId}}, upsert=False)
    
    user2 = users.find_one_and_update({'_id': ObjectId(userId)}, {'$addToSet': {'following': id}}, upsert=False)
    
    user['_id'] = str(user['_id'])
    user2['_id'] = str(user2['_id'])
    return jsonify({'data': [{'follower': user2}, {'following': user}]})

class Unfollow(Resource):
  def put(self, id):
    users = mongo.db.users
    userId = request.get_json()['userId']

    user = users.find_one_and_update({'_id': ObjectId(userId)}, {'$pull': {'followers': id}}, upsert=False)

    user2 = users.find_one_and_update({'_id': ObjectId(id)}, {'$pull': {'following': userId}}, upsert=False)

    user['_id'] = str(user['_id'])
    user2['_id'] = str(user2['_id'])
    return jsonify({'data': [{'follower': user2}, {'following': user}]})

api.add_resource(GetAllUsers, '/users')
api.add_resource(AddUser, '/users')
api.add_resource(UpdateUser, '/users/<id>')
api.add_resource(DeleteUser, '/users/<id>')
api.add_resource(Login, '/users/login')
api.add_resource(Follow, '/users/<id>/follow')
api.add_resource(Unfollow, '/users/<id>/unfollow')