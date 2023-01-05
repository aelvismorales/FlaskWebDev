from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
from flask import current_app
import jwt
import datetime

login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
db=SQLAlchemy()


class User(UserMixin,db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),unique=True,nullable=False,index=True)
    password_hash=db.Column(db.String(128))
    email=db.Column(db.String(200),unique=True,index=True)
    number=db.Column(db.String(20),default="999456877")
    role_id=db.Column(db.Integer,db.ForeignKey("roles.id"))
    confirmed=db.Column(db.Boolean,default=False)
    @property
    def password(self):
        raise AttributeError('password is not readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    def generate_confimation_token(self,expiration=3600):
        reset_token=jwt.encode({"confirm":self.id,
                                "exp":datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(seconds=expiration)},
                                current_app.config['SECRET_KEY'],
                                algorithm="HS256")
        return reset_token
    def confirm(self,token):
        try:
            data= jwt.encode(token,current_app.config['SECRET_KEY'],leeway=datetime.timedelta(seconds=10),algorithm=["HS256"])
        except:
            return False
        if data.get('congirm')!= self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True

class Roles(db.Model):
    __tablename__="roles"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    users=db.relationship('User',backref='role')

    def __init__(self, name):
        self.name=name