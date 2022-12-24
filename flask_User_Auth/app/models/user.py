from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),unique=True,nullable=False)
    password_hash=db.Column(db.String(128))
    email=db.Column(db.String(200))
    number=db.Column(db.String(20),default="999456877")

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
    