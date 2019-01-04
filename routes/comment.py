from app import app, mongo
from flask_restful import Resource, Api
from flask import jsonify, request
from bson.objectid import ObjectId

api = Api(app)

class AddComment(Resource):
  def post(self):
    comments = mongo.db.comments
    name = request.get_json()['name']
    comment = request.get_json()['comment']

    name_id = comments.insert(
      {
        'name': name,
        'comment': comment
      }
    )

    new_comment = comments.find_one({'_id': name_id})

    result = {
      'username': new_comment['name'],
      'comment': new_comment['comment'],
      'message': 'comment was created successfully'}

    return jsonify({'data': result})

class UpdateComment(Resource):
  def put(self, id):
    comments = mongo.db.comments
    comment = request.get_json()['comment']

    comments.find_one_and_update({'_id': ObjectId(id)}, {'$set': {'comment': comment}}, upsert=False)
    new_comment = comments.find_one({'_id': ObjectId(id)})

    result = {'username': new_comment['comment'], 'message': 'comment was updated successfully'}

    return jsonify({'data': result})

api.add_resource(AddComment, '/api/comments')
api.add_resource(UpdateComment, '/api/comments/<id>')