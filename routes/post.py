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
          'userId': field['userId'],
          'mainTimer': field['mainTimer'],
          'distance': field['distance'],
          'coords': field['coords'],
          'likes': field['likes'],
          'comments': field['comments'],
        }
      )
    return jsonify(data)
  
class DeletePost(Resource):
  def delete(self, id):
    posts = mongo.db.posts

    response = posts.delete_one({'_id': ObjectId(id)})

    if response.deleted_count == 1:
      result = {'message': 'post deleted successfully'}
    else:
      result = {'message': 'failed to delete post'}

    return jsonify({'data': result})

class AddPost(Resource):
  def post(self):
    posts = mongo.db.posts
    userId = request.get_json()['userId']
    mainTimer = request.get_json()['mainTimer']
    distance = request.get_json()['distance']
    coords = request.get_json()['coords']
    likes = request.get_json()['likes']
    comments = request.get_json()['comments']

    post_id = posts.insert(
      { 
        'userId': userId,
        'mainTimer': mainTimer,
        'distance': distance,
        'coords': coords,
        'likes': likes,
        'comments': comments
      }
    )
    
    new_post = posts.find_one({'_id': post_id})

    result = {
      'postId': str(new_post['_id']),
      'userId': new_post['userId'],
      'mainTimer': new_post['mainTimer'],
      'distance': new_post['distance'],
      'coords': new_post['coords'],
      'likes': new_post['likes'],
      'comments': new_post['comments'],
      'message': 'post was created successfully'
    }

    return jsonify({'data': result})

api.add_resource(GetAllPosts, '/posts')
api.add_resource(AddPost, '/posts')
api.add_resource(DeletePost, '/posts/<id>')
