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
