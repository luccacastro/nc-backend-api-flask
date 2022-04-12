from  api import db 
import time


# Migrate(app, db)

# engine = SQLAlchemy.create_engine(SQLAlchemy, sa_url=db_name, engine_opts={})
# if not database_exists(engine.url):
#     create_database(engine.url)


user_subpage = db.Table('user_subpage',
    db.Column('user_id', db.String(50), db.ForeignKey('users.name')),
    db.Column('subpage_id', db.String(), db.ForeignKey('subpage.title'))                         
)

class Users(db.Model):
    __table_args__ = (
        db.UniqueConstraint('name'),
        db.UniqueConstraint('email'),
        db.UniqueConstraint('phone'),
        db.UniqueConstraint('id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.Text)
    phone = db.Column(db.String(50))
    avatar_url = db.Column(db.Text)
    rank = db.Column(db.String(50))
    created_at = db.Column(db.Integer, default=int(time.time()))
    post = db.relationship('Post', backref='users')
    comment = db.relationship('Comment', backref='users')
    following = db.relationship('Subpage', secondary=user_subpage, backref='followers')
    def as_dict(self):
           return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    # def __repr__(self):
    #     return '<User {}>'.format(self.title)
    
class Subpage(db.Model):
    __table_args__ = (
        db.UniqueConstraint('id'),
        db.UniqueConstraint('title')
    )
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.Integer, default=int(time.time()))
    post = db.relationship('Post', backref='subpage')
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    # followed = db.relationship('Subpage', secondary=user_subpage, backref='followed')

    # user = db.relationship('User', backref='subpage')

class Post(db.Model):
    __table_args__ = (
         db.UniqueConstraint('id'),
        db.UniqueConstraint('ref_id'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False, )
    is_blurred = db.Column(db.Boolean, default=False)
    ref_id = db.Column(db.String(50))
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_styled = db.Column(db.Text)
    author = db.Column(db.String(50), db.ForeignKey('users.name'), nullable=False)
    media_type = db.Column(db.String(12))
    media_link = db.Column(db.Text)
    votes = db.Column(db.Integer)
    subpage_name = db.Column(db.String(50), db.ForeignKey('subpage.title'), nullable=False)
    created_at = db.Column(db.Integer, default=int(time.time()))
    comment = db.relationship('Comment', backref='post')
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_styled = db.Column(db.Text)
    parent_comment_id = db.Column(db.String(50))
    ref_id = db.Column(db.String(50))
    post_id = db.Column(db.String(50), db.ForeignKey('post.ref_id'), nullable=False)
    author = db.Column(db.String(50), db.ForeignKey('users.name'), nullable=False)
    votes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Integer, default=int(time.time()))
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db.create_all()
print('end')
# subpage1 = Subpage(title='surrealmemes', description='memes from a alternate reality', created_at=None)
# subpage2 = Subpage(title='funny', description='funny memes', created_at=None)
# user = Users.query.all()[0]

# user = Users(name='inconvenient_w', email='luccazutin@gmail.com', phone='+44 079891234', avatar_url='img.ur/3ksdwd21', rank='Mod', created_at=None)
# user1 = Users(name='resourceful_lobster', email='fethc@gmail.com', phone='+44 90123442', avatar_url='img.ur/3ksdwd21', rank='Mod', created_at=None)

# user.following.append(subpage1)
# user.following.append(subpage2)
# db.session.add_all([subpage1])
# db.session.commit()
# print(user.following)
# print(subpage1.followers)
# post = Post(ref_id='u3jk120', media_type='text', media_link='youtube.com/43241', title='this is my first post', body='hello there everyone!', users=user, subpage=subpage2, created_at=None)
# comment = Comment(body='This sucks ass', parent_comment_id='hello', ref_id='ytf1023', post=post, user=user, votes=None, created_at=None)


# db.session.add_all([user, subpage1, comment, post])
# db.session.commit()


# print(post.subpage.title)
# subpage1 = Subpage.query.filter_by(title='surrealmemes').all()[0]
# print(user.post[0], subpage1.post[0].comment[0].body)
