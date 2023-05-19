from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User #import from our databases
#For creating the password hash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth",__name__)

@auth.route('/login',methods = ['GET','POST'])  #methods defines what type of requests we can get
#Below is dealing wit signifying that a user has an account, and they want to login
def login():    
    if request.method == 'POST':
        #Getting the users email and password from the submitted form
        email = request.form.get('email')
        password = request.form.get('password')

        #Looking for a specific entry in the database (do they alreayd have an account)
        user = User.query.filter_by(email=email).first() #Find the user that has the same email as the one submitted
        #If we did find a user, check the password is equal to the hash
        if user:
            if check_password_hash(user.password,password): #Checking passwords
                flash('Logged in Successfully',category = 'success') #Flash successful login
                #Keep note of the user we are logging in
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password',category='error')
        else:
            flash('An account with that email hasn/t been registered yet',category = 'error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required    #must be logged in to access this route
#Logs out the user
def logout():
    flash('Logged Out',category='success')
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register',methods = ['GET','POST'])
def register():
        #Getting the information that is sent in the form
    #Checking if the method is a POST request
    email = ''
    first_name = ''
    if request.method == 'POST':
        #If it is a POST, get the email and password
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #specific checks to see if username and password meets out requirements
        user = User.query.filter_by(email=email).first() #Checking to see if the user already exists
        if user:
            flash("There is already an account registered with this email",category="error")
        elif len(email) < 4:
            #Showing error or success messages using flash
            flash("Email must be greater than 3 characters", category="error")
        elif len(first_name) < 2:
            flash("Firstname must be greater than 1 character", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(password1) < 7:
            flash("Passwords must be greater than 6 characters", category="error")
        else:
            #add user assuming everything else is correct
            new_user =  User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'))
            #adding to DB
            db.session.add(new_user)
            #update the db
            db.session.commit()
            #Note the user that is logging in
            login_user(new_user,remember=True)
            flash("Account created!",category="success")
            #On successful registration, we want to sign them in and redirect them to the homepage
            return redirect(url_for('views.home'))
        
    return render_template("register.html",user=current_user,email=email,first_name=first_name)
