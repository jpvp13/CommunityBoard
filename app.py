import re
from typing import Text
from flask import Flask, redirect, url_for, request,render_template, json, flash, g
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login.utils import login_required, logout_user
import flask_security
from flask_security.utils import hash_password, verify_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import url,create_engine
from sqlalchemy.orm import session, sessionmaker, relationship
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user,login_manager, LoginManager
from sqlalchemy.sql.schema import MetaData
from werkzeug.datastructures import Accept
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from sqlalchemy.sql import text
from flask_security import Security, SQLAlchemyUserDatastore,  SQLAlchemySessionUserDatastore, UserMixin, RoleMixin, LoginForm, RegisterForm
import gc
from flask_admin import helpers as admin_helpers
# import hashlib import pbkdf2_sha512
from passlib.hash import sha256_crypt

from database import db_session, init_db, sessionmaker
from models import User, Role

userTable = User

app = Flask(__name__, static_url_path='', static_folder='')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config['SECURITY_PASSWORD_SALT'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.'
# app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'  
# app.config['SECURITY_LOGIN_URL'] = '/login'
# app.config['SECURITY_POST_LOGIN_VIEW'] = '/lobby'
# app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login.html'  #overriding flask-securitys default login page


app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# engine = create_engine('sqlite:///app.db', echo = True)


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Course Information', template_mode='bootstrap3')

login_manager = LoginManager() 
login_manager.init_app(app) 
login_manager.login_view = '/'

db = SQLAlchemy(app)

# Session = sessionmaker(app)
# session = Session()

class CustomLoginForm(LoginForm):
    def validate(self):
        response = super(CustomLoginForm, self).validate()
        
        return response

user_datastore = SQLAlchemySessionUserDatastore(db_session,User, Role)
security = Security(app, user_datastore, login_form = CustomLoginForm)

admin.add_view(ModelView(User, db_session))
admin.add_link(MenuLink(name='logout', category='', url="/"))



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
#     init_db()
#     user_datastore.create_user(email='test', firstName = 'John', lastName = 'Villalvazo', password= '11')
#     db_session.commit()






# def is_authenticated():
#     return True
#     # return None

# def is_active():   
#     return True           

# def is_anonymous():
#     return False          

# def get_id(user_id):         
#     return str(user_id)



# @app.before_request
# def before_request():
#     g.user = current_user


@app.route('/')
# @login_required
def startPage():
    print("starting place")
    
    return render_template('welcomePage.html')


@app.route('/path', methods = ['POST', 'GET'])
def path():
    if request.method == 'GET':
    # return 'hello'
        return render_template('login.html')

    elif request.method == 'POST':
        return render_template('signup.html')
    

    
@app.route('/login', methods = ['POST'])
def loginPage():
    
    # return "im confused"
    
    if current_user.is_authenticated:
        return render_template('signup.html')
    
    # print("I am confused")
    if request.method == 'POST':
        # EMAIL = request.form.get('email')
        USERNAME = request.form.get('username')
        PASSWORD = request.form.get('pass')
        
        
        hashedPassword = sha256_crypt.encrypt(PASSWORD)
        print(hashedPassword)
        
        
        user = userTable.query.filter_by(username = USERNAME, password = hashedPassword).first() 
        
        checkedPassword = sha256_crypt.verify(PASSWORD, hashedPassword)
        print("#####################  " + str(checkedPassword) + "\n")
        
        # if str(User.password) == str(hashedPassword):
        if checkedPassword == True:
            init_db()
            # user = user_datastore.
            # user = db.User.filter_by(username = USERNAME, password = hashedPassword).first() 
            # user = User.query.filter_by(username = USERNAME, password = hashedPassword).first() 
            print("s##################################### User  " + str(user))

            login_user(user)
            # return render_template('lobby.html')
            return redirect(url_for('lobby'))
        else:
            return "<p> Incorrect credentials, please try again</p>"
            
        
    # # gc.collection()
    # # return render_template("login.html")
    
    return render_template("whiteboard1.html")

    # return render_template('login.html')

@app.route('/signup', methods = ['POST'])
def signup():
    
    # form = RegistrationForm(request.form)
    

    
    print("inside of signup")
    if request.method == 'POST':
        print("inside of if statement")

        EMAIL = request.form.get('email')
        USERNAME = request.form.get('username')
        PASSWORD = request.form.get('pass')
        FIRSTNAME = request.form.get('firstName')
        LASTNAME = request.form.get('lastName')
        
        hashedPassword = sha256_crypt.encrypt(PASSWORD)
        print(hashedPassword)
                
        user = User.query.filter_by(email = EMAIL, username = USERNAME, password = hashedPassword).first() 

        print("USERNAME " + User.username)
        
        
        #! need to make this error more graceful
        # if User.username == USERNAME:
        #         return ('<p>The entered username already exsist</p>')
        # elif User.email == EMAIL:
        #     return ('<p>The entered email already exsist</p>')
        if not user: #checks to see if user is not unique
            init_db()
            user_datastore.create_user(email=EMAIL, username = USERNAME, firstName = FIRSTNAME, lastName = LASTNAME, password= hashedPassword)
            db_session.commit()
            db_session.close()
            # gc.collect()
            
            # login_user(user)
            return render_template('lobby.html')
            # return redirect(url_for('lobby')) #!this doesnt like to work?
            
        

    print("outside of everything")

    # return "im outside now"
    
    return render_template('signup.html')



@app.route('/lobby')
@login_required
def lobby():
    return render_template('lobby.html')




@login_manager.user_loader 
def load_user(user_id): 
    try:
        return User.query.get(user_id)
    except:
        return None
    
    

if __name__ == '__main__':
    app.run()
    