from typing import Text
from flask import Flask, redirect, url_for, request,render_template, json, flash, g
# from flask.globals import current_app
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
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import Security, SQLAlchemyUserDatastore,  SQLAlchemySessionUserDatastore, UserMixin, RoleMixin, LoginForm, RegisterForm
from flask_admin import helpers as admin_helpers
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey
from flask_login import current_user, login_user,login_manager, LoginManager
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from flask_mysqldb import MySQL


app = Flask(__name__, static_url_path='', static_folder='')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '\xfd{H\xe5<'
# app.config['SECURITY_PASSWORD_SALT'] = '.5\xd1\x01O<!\xd5\xa2\xa0\x9fR'
app.config['SECURITY_PASSWORD_SALT'] = 'CSE106'



# app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'


app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
engine = create_engine('sqlite:///app.db', echo = True)



# app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jpvptest:123456789CSE@jpvptest.mysql.pythonanywhere-services.com/jpvptest$mysqlDatabase'
# engine = create_engine('mysql+pymysql://jpvptest:123456789CSE@jpvptest.mysql.pythonanywhere-services.com/jpvptest$mysqlDatabase', echo = True)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@localhost/newDB'
# engine = create_engine('mysql+pymysql://root:0000@localhost/newDB', echo = True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
engine = create_engine('sqlite:///app.db', echo = True)


# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'

socketio = SocketIO(app)
# socket = socketio.Server()
# app = socketio.WSGIApp(socket)

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
    # password = Column(db.String)  #no size specified
    password = Column(db.Text)  #no size specified
    bio = Column(db.Text, nullable=True)

    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))

    def __init__(self, email, username, password, bio):
        self.email = email
        self.username = username
        self.password = password
        self.bio = bio

    def is_authenticated(self):
        return True
        # return None

    def is_active(self):   
        return True    


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

admin.add_view(AdminView(RolesUsers, db_session))
admin.add_view(AdminView(Role, db_session))
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
    
#     hashedPassword = generate_password_hash('00')
    
#     user_datastore.create_user(email='admin@admin.com', username = 'admin', password= hashedPassword, bio = "This is the main admin account!")
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
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    print("you have been logged out")
    return redirect('/')
    # return redirect(url_for('/'))

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

    if request.method == 'PUT':
        print('signup here')
        return render_template('signup.html')

    elif request.method == 'POST':
        
        checkedPassword = False
        
        USERNAME = request.form.get('username')
        PASSWORD = request.form.get('password')
        
        print("Im going to check out database")
        user = User.query.filter_by(username = USERNAME).first()
        print("Nothing came up in the database")

        if not user :
            print("THIS PERSON DOESNT EXIST")
            message = "Incorrect username or password"
            return render_template("welcomePage.html", error = message)

        hashedPassword = generate_password_hash(PASSWORD, method="pbkdf2:sha256", salt_length= 4)
        checkedPassword = check_password_hash(user.password, PASSWORD)
        
        
        print("#############################################")
        print("This is the hashed password: " + hashedPassword)
        print("Password match? " + str(checkedPassword))

        # print("The current user is: " + user.username)
        
        
        
        if USERNAME == 'admin' and checkedPassword == True:
            
            login_user(user)

            return redirect('/admin')
        
        elif user and checkedPassword == True:
            
            
            if current_user.is_authenticated:
                # print("The curent user is authorized?  -- " + current_user.is_authorized)
                print("im already authorized!")
                return render_template('whiteboard1.html')
            
            login_user(user)
            # return redirect(url_for('lobby'))     #!main place this will redirect to, but can be changed to different places
            return render_template('whiteboard1.html')
        
            # return "<p> Incorrect credentials, please try again</p>"
            
        
        
    # return redirect(url_for('login'))
    return render_template('welcomePage.html')

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
        # print("inside of if statement")

        EMAIL = request.form.get('email')
        USERNAME = request.form.get('username')
        PASSWORD = request.form.get('password')

        
        hashedPassword = generate_password_hash(PASSWORD, method="pbkdf2:sha256", salt_length= 4)
 
        print(hashedPassword)
        
        #initial check to see if user with same info exsists
        user = User.query.filter_by(username = USERNAME, password = hashedPassword, email = EMAIL).first()


        #checking to see if user is attempting to make a admin account
        if USERNAME == "admin" or USERNAME == "administrator" or USERNAME == "Admin" or USERNAME == "ADMIN":
             print("uhh u cant do that")
             message = "invalid input"
             return render_template("signup.html", error = message)
            
            
        if user: #checks to see if user is unique, errors out by saying username must be unique
            print('AHHHHHHHHHHHH')
        
            message = "This username already exists"
            # message = "FIX ME, I AM UNREADABLE"
            return render_template("signup.html", error = message)
        else :
            
            print("I am attempting to creating a new user now...")
            
            #since username is only unique value, then we check again in case something changes while transiitoning from login->signup
            checkingUser = User.query.filter_by(username = USERNAME).first()
            
            #check to see if user is attempting to make a username with no characters
            if len(USERNAME) == 0:
                print('attempting to make a user with no info')
                message = "Enter a username"
                # message = "FIX ME, I AM UNREADABLE"
                return render_template("signup.html", error = message)
            
            elif checkingUser:
                message = "This username already exists"
                # message = "FIX ME, I AM UNREADABLE"
                return render_template("signup.html", error = message)
                # return "<p> This username already exists. Please enter a different username. </p>"
                
            else:
            
                # newUser = User(EMAIL, USERNAME, hashedPassword)
                db.session.add(User(EMAIL, USERNAME, hashedPassword, None))
                db.session.commit()
                db.session.close()
            
                print("New user has been created")
                
                newUser = User.query.filter_by(username = USERNAME, password = hashedPassword, email = EMAIL).first()
                
                login_user(newUser)    #since we just push the person into the app after creating a user
         
                return render_template("whiteboard1.html")
        
            
            
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
    # print('username->' + current_user.username)
    # emit('my response', {'message': '{0} has joined'.format(current_user.username)}, broadcast=True)

def some_function():
    socketio.emit('some event', {'data': 42})
    
client_count = 0 
    
@socketio.on('connect')
def connected():
    global client_count
    client_count += 1
    print(current_user.username, '--CONNECTED!--')
    socketio.emit('client_count', client_count)
    
@socketio.on('disconnect')
def disconnected():
    global client_count
    client_count -= 1
    print(current_user.username, '--DISCONNECTED--')
    socketio.emit('client_count', client_count)

@socketio.on('Canvas Updated')
def value_changed(message):
    
    socketio.emit('update value', message, broadcast=True)

@socketio.on('Clear Clicked')
def clicked(message):
    socketio.emit('update clear', message, broadcast=True)
    
# @socketio.event
# def connect(sid, environ):
#     print(sid, 'connected!!!')
    
# @socketio.event
# def disconnect(sid):
#     print(sid, 'disconnected!!!')
    
# @socketio.on('join')
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send(username + ' has entered the room.', to=room)
    
# def websocket_app(environ, start_response):
#     if environ["PATH_INFO"] == '/echo':
#         ws = environ["wsgi.websocket"]
#         message = ws.receive()
#         ws.send(message)

# @sock.route('/echo')
# def echo(ws):
#     while True:
#         data = ws.receive()
#         ws.send(data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',cors_allowed_origins="*")
    # app.run()
