from . import db #import the db object
from flask_login import UserMixin #Custom class gives user object usefull things
from sqlalchemy.sql import func

class Chat(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    #Need to associate notes with each user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #user.id = the id field of our user class
    

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True) #cant have an emaiul that already exists
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #From all users, we want t obe able to find all their notes
    chats = db.relationship('Chat')