from models import Users, Post, Comment, Subpage
import requests


posts = Post.query.filter_by(media_type='link').all()
for post in posts:
    print(post.as_dict()['body'])
    # print(post.as_dict()['media_link'])
    # post = requests.get()
    if post.as_dict()['media_link']:
        r = requests.get(post.as_dict()['media_link'])
        print(r, post.as_dict()['media_link'].endswith('.png'), post.as_dict()['media_link'])