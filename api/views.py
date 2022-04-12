from importlib.abc import ResourceReader
from flask import Flask, abort, jsonify, request
from flask_restful import Api, Resource, reqparse
# from models import Users, Post, Comment, Subpage
from api import app, db
import random, string

api = Api(app)




# get random string of letters and digits
def generateRefId(contentType):
   initial_letter = 't' if contentType == 'post' else 'i'
   source = (string.ascii_letters + string.digits).lower()
   result_str = ''.join((random.choice(source) for i in range(5)))
   return '{0}{1}'.format(initial_letter, result_str)

def getUser(name):
   return Users.query.filter_by(name=name).first()

def getSubpage(title):
   return Subpage.query.filter_by(title=title).first()

def getPost(ref_id):
   return Post.query.filter_by(ref_id=ref_id).first()

def getComment(ref_id):
   return Comment.query.filter_by(ref_id=ref_id).first()


class UserData(Resource):
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

class SubPageData(Resource):
   def get(self,title):
      
      subpage = Subpage.query.filter_by(title=title).all()[0]
      posts = [post.as_dict() for post in subpage.post]
      subpage_data = subpage.as_dict()
      total_suscribed_users = len(subpage.followers)
      return {
         'subpage':{
            'name': subpage_data['title'],
            'description':  subpage_data['description'],
            'subscribed_users': total_suscribed_users,
            'posts': posts
         }
      }
         
class getAllSubPages(Resource):
   def get(self):
      subpage = Subpage.query.all()
      subpage = [sub.as_dict() for sub in subpage]
      return {
         'sublist': subpage
      }
      
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
         # post_data['id'] = int(db.session.query(Post).count())+1
         post_obj = Post(**post_data, users=user, subpage=subpage)
         # print(post_obj.as_dict())
         db.session.add(post_obj)
         db.session.commit()
         return post_data
         
         
   
class getPostSamples(Resource):
      def get(self):
         print(request.args)
         if request.args:
            # sample = int(request.args['limit']) if request.args['limit'] == None else 20
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
            # print()
            # rand = random.randrange(int(Post.query.first().as_dict()['id']), int(db.session.query(Post).count())+int(Post.query.first().as_dict()['id']))
            rand = random.randrange(0, int(db.session.query(Post).count()))
            post_sample = Post.query.all()[rand]
            post_obj = post_sample.as_dict()
            post_obj['num_comments'] = len(post_sample.comment)
            post_list.append(post_obj)  
         return post_list   

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



api.add_resource(UserData, '/api/username/<string:name>', )
api.add_resource(SubPageData, '/api/subpage/<string:title>')
api.add_resource(getAllSubPages, '/api/subpage/')
api.add_resource(getPostData, '/api/post/<string:ref_id>')
api.add_resource(createPost, '/api/post/add')
api.add_resource(getPostSamples, '/api/post/sample')
api.add_resource(PostComments, '/api/post/<string:post_id>/comments')
api.add_resource(changeContentScore, '/api/voting/')


