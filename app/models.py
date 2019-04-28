from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String(80), index = True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(1000))
    profile_pic_path = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    blogs = db.relationship('Blog', backref = 'user', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

class Blog(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key = True)
    post_title = db.Column(db.String)
    post_content = db.Column(db.String)
    photo_path = db.Column(db.String(255))
    category = db.Column(db.String, nullable = False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref = 'blog', lazy = 'dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls, category):
        blogs = cls.query.filter_by(category = category).all()
        return blogs

    @classmethod
    def get_blog(cls, id):
        blog = cls.query.filter_by(id = id).first()
        return blog

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(255))
    date = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = cls.query.filter_by(blog_id = id).all()
        return comments

    @classmethod
    def delete_comment(cls, id):
        comment = cls.query.filter_by(id = id).first()
        db.session.delete(comment)
        db.session.commit()

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(), unique = True)