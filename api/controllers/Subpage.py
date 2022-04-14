from models import Subpage
from flask_restful import Resource

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