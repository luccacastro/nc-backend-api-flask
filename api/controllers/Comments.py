from models import Comment, Post
from api.utils import getPost, getUser
from flask_restful import Api, Resource, reqparse
from flask import abort
from api import db

class PostComments(Resource):
    def get(self, post_id):
      post = Post.query.filter_by(ref_id=post_id).first()
      if post:
         comments = [ comment.as_dict() for comment in post.comment]
         return {"post_id": post.as_dict()['id'], "comments": comments}
      else:
         abort(404, "Couldn't find any posts with such id")
   
    def post(self, post_id):
        parser = reqparse.RequestParser()
        parser.add_argument('post', type=str)
        parser.add_argument('body', type=str)
        parser.add_argument('body_styled', type=str)
        parser.add_argument('users', type=str)
        parser.add_argument('ref_id', type=str)
        parser.add_argument('parent_comment_id', type=str)
        # parser.add_argument('media_type', type=str)
        # parser.add_argument('media_link', type=str)
        parser.add_argument('votes', type=id)
        parser.add_argument('created_at', type=str)
        args = parser.parse_args()
        print(args)
        user = getUser(args['users'])
        post = getPost(args['post'])
        comment_data = {**args, 'users': user, 'post':post, 'votes': None, 'created_at': None}
        print(comment_data)
        comment_obj = Comment(**comment_data)
        db.session.add(comment_obj)
        db.session.commit()