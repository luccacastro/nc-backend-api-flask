from flask_restful import Api, Resource, reqparse
from flask import Flask, abort, jsonify, request
from models import Post
from api import app, db
from api.utils import generateRefId, getPost, getComment, getSubpage,getUser
import random

class getPostData(Resource):
      def get(self, ref_id):    
         post = Post.query.filter_by(ref_id=ref_id).first()
         if post:
            comments = [ comment.as_dict() for comment in post.comment]
            post_data = post.as_dict()
            return {**post_data, 'num_comments': len(post.comment), 'comments': comments}
         else:
            abort(404, "Post does not exist")
            
class createPost(Resource):
      def post(self):
         parser = reqparse.RequestParser()
         parser.add_argument('title', type=str)
         parser.add_argument('body', type=str)
         parser.add_argument('body_styled', type=str)
         parser.add_argument('users', type=str)
         parser.add_argument('media_type', type=str)
         parser.add_argument('media_link', type=str)
         parser.add_argument('votes', type=id)
         parser.add_argument('subpage', type=str)
         args = parser.parse_args()
         user = getUser(args['users'])
         subpage = getSubpage(args['subpage'])
         post_data = {'title': args['title'], 
                     'body': args['body'], 
                     'body_styled': args['body_styled'],
                     'media_type': args['media_type'],
                     'media_link': args['media_link'],
                     'votes': 0, 
                     'ref_id':  generateRefId('post'), 
                     }
         post_obj = Post(**post_data, users=user, subpage=subpage)
         db.session.add(post_obj)
         db.session.commit()
         return post_data

   
class getPostSamples(Resource):
      def get(self):
         print(request.args)
         if request.args:
            sample = 60
            subpage = request.args['topic']
            upvoteOrder = request.args.get('votes')
            commentOrder = request.args.get('comment')
         else:
            sample = 60
            subpage = None
         if isinstance(sample, int):
            if subpage:
               subpageContent = Post.query.filter_by(subpage_name=subpage).all()[0:30]
               print(subpage)
               post_list = [{**post.as_dict(), 'num_comments': len(post.comment)} for post in subpageContent]
            else:
               post_list = self.getRandomPosts(sample)
            return jsonify({"post_sample": post_list})
         else:
            abort(400, 'limit has to be a number')
               
      def getRandomPosts(self, sample):
         post_list = []
         for i in range(0, sample):
            rand = random.randrange(0, int(db.session.query(Post).count()))
            post_sample = Post.query.all()[rand]
            post_obj = post_sample.as_dict()
            post_obj['num_comments'] = len(post_sample.comment)
            post_list.append(post_obj)  
         return post_list   



