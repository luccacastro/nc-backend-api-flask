from flask_restful import Resource, reqparse
from models import Comment, Post
from flask import abort
from api import db


class changeContentScore(Resource):
    def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('contentType', type=str)
      parser.add_argument('ref_id', type=str)
      parser.add_argument('increaseScore', type=bool)   
          
      args = parser.parse_args()
      contentType = args['contentType']
      ref_id = args['ref_id']
      increaseScore = args['increaseScore']
      models = {
         "post": Post,
         "comment": Comment
      }
      if models.get(contentType):  
         content = models[contentType].query.filter_by(ref_id=ref_id).first()
         if content:       
            vote = 1 if increaseScore else -1
            content.votes = content.votes + vote
            db.session.commit()
            return models[contentType].query.filter_by(ref_id=ref_id).first().as_dict()
         else:
            abort(400, "Couldn't find any comments/posts with such id")
      else:
         abort(400, 'Bad request, invalid content type')