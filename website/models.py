from . import db #import the db object
from flask_login import UserMixin #Custom class gives user object usefull things
from sqlalchemy.sql import func

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(50000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # user.id is case-sensitive and depends on your User model

    

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True) #cant have an emaiul that already exists
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #From all users, we want t obe able to find all their notes
    chats = db.relationship('Chat')