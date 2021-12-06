from re import X
from typing import Text
from flask import Flask, redirect, url_for, request,render_template, json, flash, g
from flask.globals import current_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_login.utils import login_required, logout_user
from flask_security.datastore import UserDatastore
from flask_security.forms import Email
from flask_security.utils import encrypt_password, hash_password, verify_hash, verify_password
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import url,create_engine
from sqlalchemy.orm import session, sessionmaker, relationship
from flask_admin.contrib.sqla import ModelView
# from sqlalchemy.sql.schema import MetaData
# from werkzeug.datastructures import Accept
from werkzeug.security import generate_password_hash, check_password_hash
# from wtforms import Form, BooleanField, StringField, PasswordField, validators
# from sqlalchemy.sql import text
from flask_security import Security, SQLAlchemyUserDatastore,  SQLAlchemySessionUserDatastore, UserMixin, RoleMixin, LoginForm, RegisterForm
from flask_admin import helpers as admin_helpers
# import hashlib import pbkdf2_sha512
# from passlib.hash import sha256_crypt
# from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, send, emit

# from database import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey
from flask_login import current_user, login_user,login_manager, LoginManager
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__, static_url_path='', static_folder='')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '\xfd{H\xe5<'
app.config['SECURITY_PASSWORD_SALT'] = '.5\xd1\x01O<!\xd5\xa2\xa0\x9fR'

app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'  
# app.config['SECURITY_LOGIN_URL'] = '/login'
# app.config['SECURITY_POST_LOGIN_VIEW'] = '/lobby'
# app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login.html'  #overriding flask-securitys default login page



app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
engine = create_engine('sqlite:///app.db', echo = True)
# engine = create_engine('sqlite:///app.db', echo = True)


# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'

socketio = SocketIO(app)

login_manager = LoginManager(app) 
login_manager.init_app(app) 
login_manager.login_view = 'login'

db = SQLAlchemy(app)

# bcrypt = Bcrypt(app)

Session = sessionmaker(app)
session = Session()

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()





# class RolesUsers(Base):
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', db.Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', db.Integer(), ForeignKey('role.id'))

# class Role(RoleMixin, Base):
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(db.Integer(), primary_key=True)
    name = Column(db.String(80), unique=True)
    description = Column(db.String(255))
    
    
# class User( UserMixin, Base):
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(255), unique=True)
    username = Column(db.String(255), unique = True)
    password = Column(db.String)  #no size specified
    firstName = Column(db.String(255))
    lastName = Column(db.String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(db.String(100))
    current_login_ip = Column(db.String(100))
    login_count = Column(db.Integer())
    active = Column(db.Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))
    
    
   
class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return current_user.is_authenticated
        # print (session.get('username'))
        # return session.get('username') == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('startPage', next=request.url))

class CustomLoginForm(LoginForm):
    def validate(self):
        response = super(CustomLoginForm, self).validate()
        
        return response

user_datastore = SQLAlchemySessionUserDatastore(db_session,User, Role)
security = Security(app, user_datastore, login_form = CustomLoginForm)


admin = Admin(app, name='Dashboard', template_mode='bootstrap3', index_view= AdminView(User, db.session, url = '/admin', endpoint = '/logout'))

# admin.add_view(AdminView(User, db_session))
admin.add_view(AdminView(RolesUsers, db_session))
admin.add_view(AdminView(Role, db_session))
# admin.add_view(ModelView(User, db_session))
# admin.add_view(ModelView(RolesUsers, db_session))
# admin.add_view(ModelView(Role, db_session))
admin.add_link(MenuLink(name='logout', category='', url="/logout"))



@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template = admin.base_template,
        admin_view = admin.index_view,
        h = admin_helpers,
        get_url = url_for
    )

# @app.before_first_request
# def create_user():
#     db.create_all()
#     # init_db()
#     # db.add(email='test', username = 'm', firstName = 'John', lastName = 'Villalvazo', password= '11')
#     user_datastore.create_user(email='test', username = 'a', firstName = 'John', lastName = 'Villalvazo', password= 'a')
#     # db.session.add_all(email='test', username = 'm', firstName = 'John', lastName = 'Villalvazo', password= '11')
#     db_session.commit()
#     db_session.close()
#     # db.commit()





#! code starts here so user can select what they want to do
@app.route('/')
def startPage():
    print("starting place")
    # db.create_all()
    return render_template('welcomePage.html')
    # return render_template('login.html')

#! This portion will alow for a user to log out, only works if they have signed in
@app.route('/logout')
@login_required
def logout():
    logout_user()
    
    
    
    
    print("you have been logged out")
    return redirect(url_for('/'))

@app.route('/adminView')
@login_required
def adminPage():
    # return redirect(url_for('authenticatedAdmin.index'))
    return redirect('/admin')


#! this code block will display the apporpriate html page based on users choice within welcomePage.html
@app.route('/path', methods = ['GET'])
def path():
    if request.method == 'GET':
        return render_template('signup.html')
    

#! this is where a users info will go when logging in. The code will first check to see if the user
#! is already authenticated (aka if you refresh the page and come back it should just let the person to continue
#! were they were).
#! The if not authenticated, it will get their info, hash their password and compare it to whats in our db,
#! as well as checking to see if the user with their UNIQUE username also appear in our db

#! If these both return True, then code "login_user(user)" will run, and will assign user a token that will let them
#! go in and out of our apps protected pages (again it SHOULD... after 23 hours i'm fried and not sure lol), if either dont
#! match, then a error pops up saying "incorrect credentials" which we should change in future iteration

#! else if none of these checks are met, it will just return user to the login page
@app.route('/login', methods = ['POST', 'PUT'])
def loginPage():
    
    # return "im confused"
    
    


    if request.method == 'PUT':
        print('signup here')
        return render_template('signup.html')
        # return redirect(url_for('signup'))
        
    # elif request.method == 'GET':

    elif request.method == 'POST':
        
        
        # EMAIL = request.form.get('email')
        USERNAME = request.form.get('username')
        PASSWORD = request.form.get('pass')
        
        # test= User.query.filter_by(username = USERNAME).first() 

        
        # hashedPassword = hash_password(PASSWORD)
        # hashedPassword = encrypt_password(PASSWORD)
        hashedPassword = generate_password_hash(PASSWORD)

        # print("#########################################################")
        # print("Hashed Password")
        # print(hashedPassword)
        
        # checkedPassword = bcrypt.check_password_hash(hashedPassword, PASSWORD)
        checkedPassword = check_password_hash(hashedPassword, PASSWORD)

        # print("#########################################################")
        # print("Equal?")
        # print(test.password)
        # print(PASSWORD)
        # print(test.password == PASSWORD)

        # print("#########################################################")
        # print("Checked Password")
        # print(checkedPassword)
        
        user = User.query.filter_by(username = USERNAME).first() 


        # print("#########################################################")
        # print("###### What is this output? @@@@ ")
        print("The current user is: " + user.username)
        
        # if str(User.password) == str(hashedPassword):
        if user.username == 'admin' and checkedPassword == True:
            return redirect('/admin')
            # return redirect(url_for('admin.index'))
        
        elif user and checkedPassword == True:
            
            if current_user.is_authenticated:
                print("im already authorized!")
                
                print("This is the cirrent user: " + str(current_user))
                print(current_user.is_authenticated)
                print("Is current user active?")
                print(current_user.is_active)
                return render_template('whiteboard1.html')
            
            print("###############################################")
            print("The user who is currently logged in")
            print(current_user)
            
            login_user(user)
            # return redirect(url_for('lobby'))     #!main place this will redirect to, but can be changed to different places
            return render_template('whiteboard1.html')
        else:
            return "<p> Incorrect credentials, please try again</p>"
            
        
    # return redirect(url_for('login'))
    return render_template('login.html')

#~ this code block is used to sign a user up to our app (aka adding their info to our db). This will take in any info we want, but
#~ as a testing purpose i used the below. After this, the users entered password is hashed using werkzeug.security module which takes care of 
#~ generating a hash and checking the hashed password. After hashing the password, it will query our db to check if this infromation has already
#~ been entered into our app.

#~if the user does NOT exisit already in our db, we go ahead and add them into our db with their entered info and newly hashed password. After commiting
#~ addition into our db, we push them through to the lobby page (or anywhere else needed/wanted). If no checks are passed, then we just send them back to
#~ the signup page. Once created a account with us and pushed into app, i assume we can use the "login_user(user)" feature of flask-login since they will need 
#~ to navigate to pages once they create a account
@app.route('/signup', methods = ['POST'])
def signup():
    
    print("inside of signup")
    if request.method == 'POST':
        print("inside of if statement")

        EMAIL = request.form.get('email')
        USERNAME = request.form.get('username')
        PASSWORD = request.form.get('pass')
        FIRSTNAME = request.form.get('firstName')
        LASTNAME = request.form.get('lastName')
        
        hashedPassword = generate_password_hash(PASSWORD)
        print(hashedPassword)
        
        # hashedPassword = hash_password(PASSWORD)
        # print(hashedPassword)
                
        user = User.query.filter_by(email = EMAIL, username = USERNAME, password = hashedPassword).first() 

        # print("USERNAME " + User.username)
        
        
        #! need to make this error more graceful
        # if User.username == USERNAME:
        #         return ('<p>The entered username already exsist</p>')
        # elif User.email == EMAIL:
        #     return ('<p>The entered email already exsist</p>')
        #!
        
        if user: #checks to see if user is not unique
            return "This username already exists. Please enter a different username"
        else:
            # init_db()
            user_datastore.create_user(email=EMAIL, username = USERNAME, firstName = FIRSTNAME, lastName = LASTNAME, password= hashedPassword, )
            db_session.commit()
            db_session.close()
            # gc.collect()
            
            # login_user(user)    #! discuss with team, confirm if this is correct
            # return redirect(url_for('lobby'))
            return render_template("welcomePage.html")
        
            
            
    return render_template('signup.html')


#? This code here is meant to be used when the user has logged in or created a new account and is allowed to begin
#? using our app. This can drop the user anywhere we want, created a dummy route for now
@app.route('/lobby')
@login_required
def lobby():
    return render_template('lobby.html')

#* this code is similar to the '/lobby' route, but was just meant to test to make sure a user was authenticated
@app.route('/testing')
@login_required
def testing():
    return "Hi just testing this!"
    # return render_template('lobby.html')

#& required code to help flask-login work
@login_manager.user_loader 
def load_user(user_id): 
    return User.query.get(user_id)
    
#^ this code is meant to allow for a unauthorized user... not user if properly working at this moment
@login_manager.unauthorized_handler
def unauthorized_handler():
    
    # session.pop('logged_in', None)
    return redirect(url_for('startPage'))


@app.before_request
def before_request():
    g.user = current_user
    
    
#########################################################
###### SocketIO Stuff#########
###############################################
# @socketio.on('message')
# def handle_message(data):
#     print('received message: ' + data)
    
# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
#     return 'one', 2



@socketio.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)
    
def some_function():
    socketio.emit('some event', {'data': 42})


if __name__ == '__main__':
    # socketio.run(app)
    app.run()
    