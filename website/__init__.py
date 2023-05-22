from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#Initialise database
db = SQLAlchemy()
#Naming the database
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'andrewmichaeltatenda'
    #Telling flask we are uysing the DB and where it is located
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #Intialise db by giving it our flask app
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .chat import chat
    #from .models import User, Chat


    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(chat, url_prefix='/')


    
    #Before we run the server, we are checking if we have created the database
    from .models import User, Chat

    #Uses the function we created.
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'   #Where do  we egt redirected if we are not logged in and a login is requried 
    login_manager.init_app(app) #telling what app we are using

    #Telling flask how we load user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  #Looking for the primary key
    
    return app 

    return app

#Checks if the DB exists, if it does not, we ill we create - if it does, we leave it
def create_database(app):
    #Check if the path to our database already exists
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database')
