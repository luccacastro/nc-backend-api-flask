from flask_restful import Api, Resource, reqparse
from flask import Flask, abort, jsonify, request
from models import Users

class getSingleUser(Resource):
    def get(self, name):
         user = Users.query.filter_by(name=name).first()
         if user:
            user_data = user.as_dict()
            posts = [post.as_dict() for post in user.post]
            comment = [comment.as_dict() for comment in user.comment]
            return {
               'userdata': {
                  'avatar_url': user_data['avatar_url'],
                  'rank': user_data['rank'],
                  'created_at': user_data['created_at'],
                  'posts': posts,
                  'comment': comment
               }
            }
         else:
            abort(404, "User not found")