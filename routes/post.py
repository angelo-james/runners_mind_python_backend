from app import app, mongo
from flask_restful import Resource, Api
from flask import jsonify, request
from bson.objectid import ObjectId

api = Api(app)

class GetAllPosts(Resource):
  def get(self):
    posts = mongo.db.posts
    data = []

    for field in posts.find():
      data.append(
        {
          '_id': str(field['_id']),
          'distance': field['distance'],
          'duration': field['duration'],
          'pace': field['pace']
        }
      )
    return jsonify(data)

class AddPost(Resource):
  def post(self):
    posts = mongo.db.posts
    distance = request.get_json()['distance']
    duration = request.get_json()['duration']
    pace = request.get_json()['pace']

    post_id = posts.insert(
      {
        'distance': distance,
        'duration': duration,
        'pace': pace
      }
    )
    
    new_post = posts.find_one({'_id': post_id})

    result = {
      'distance': new_post['distance'],
      'duration': new_post['duration'],
      'pace': new_post['pace'],
      'message': 'post was created successfully'
    }

    return jsonify({'data': result})

api.add_resource(GetAllPosts, '/api/posts')
api.add_resource(AddPost, '/api/posts')