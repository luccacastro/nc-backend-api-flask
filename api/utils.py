from models import Users, Post, Comment, Subpage
import random, string


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