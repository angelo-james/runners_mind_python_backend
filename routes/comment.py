from app import app, mongo
from flask_restful import Resource, Api
from flask import jsonify, request
from bson.objectid import ObjectId

api = Api(app)

class GetAllComments(Resource):
  def get(self):
    comments = mongo.db.comments
    data = []

    for field in comments.find():
      data.append(
        {
          '_id': str(field['_id']),
          'username': field['name'],
          'comment': field['comment']
        }
      )
    return jsonify(data)

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

api.add_resource(GetAllComments, '/api/comments')
api.add_resource(AddComment, '/api/comments')