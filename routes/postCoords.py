from app import app, mongo
from flask_restful import Resource, Api
from flask import jsonify, request
from bson.objectid import ObjectId

api = Api(app)

class GetPostCoords(Resource):
  def get(self):
    postCoords = mongo.db.postCoords
    data = []

    for field in postCoords.find():
      data.append({
        'postId': field['postId'],
        'coords': field['coords']
      })
      
    return jsonify({'data': data})

class AddPostCoords(Resource):
  def post(self):
    postCoords = mongo.db.postCoords
    postId = request.get_json()['postId']
    coords = request.get_json()['coords']

    coords_id = postCoords.insert(
      { 
        'postId': postId,
        'coords': coords
      }
    )
    
    new_coords = postCoords.find_one({'_id': coords_id})

    result = {
      'coordsId': str(new_coords['_id']),
      'postId': new_coords['postId'],
      'coords': new_coords['coords'],
      'message': 'coords were inserted successfully'
    }

    return jsonify({'data': result})

api.add_resource(AddPostCoords, '/coords')
api.add_resource(GetPostCoords, '/coords')