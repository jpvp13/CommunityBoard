from enum import unique
from flask import Flask, redirect, url_for, request,render_template, json, flash, abort
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login.mixins import UserMixin
from flask_login.utils import login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import url, create_engine
from sqlalchemy.orm import session, sessionmaker, relationship
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user,login_manager, LoginManager
from sqlalchemy.sql.expression import exists
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.selectable import Exists
from werkzeug.exceptions import Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy import Table, Column, Integer, String, MetatData, ForeignKey
from sqlalchemy.sql import text
from urllib.parse import urlparse, urljoin
import hashlib
import gc

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, Email, InputRequired

metadata_ob = MetaData()


app = Flask(__name__, static_url_path='', static_folder='')
# app.config.from_object('config')
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
engine = create_engine('sqlite:///app.db', echo = True)
# # set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Course Information', template_mode='bootstrap3')
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'   #Also out salt

login_manager = LoginManager() 
login_manager.init_app(app) 
login_manager.login_view = 'login'

db = SQLAlchemy(app)

metadata_ob.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_Username = db.Column(db.String(100), unique = True, nullable = False)
    user_password = db.Column(db.String(100), nullable = False)
    user_firstName = db.Column(db.String(100), nullable = False)
    user_lastName = db.Column(db.String(100), nullable = False)
    user_type = db.Column(db.Text, nullable = False)
    user_lastColor = db.Column(db.Text, nullable = False)
    user_Bio = db.Column(db.Text, nullable = True)

    def __init__ (self, id, user_Username, user_password, user_type, user_lastColor, user_Bio,user_firstName,user_lastName):
        self.user_id = id
        self.user_Username = user_Username
        self.user_password = generate_password_hash(user_password)
        self.user_type = user_type
        self.user_lastColor = user_lastColor
        self.user_Bio = user_Bio
        self.user_lastName = user_lastName
        self.user_firstName = user_firstName
        
    # def __repre__(self):
    #     return self.user_name
    
    def is_authenticated(self):
        return True
        # return None

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(user_id):         
        return str(user_id)
    
    # def set_password(self, password):
    #     salt = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    #     plaintext = password.encode()
        
    #     digest = hashlib,hashlib.pbkdf2_hmac('sha256', plaintext, salt, 10000)
        
    #     hex_hash = digest.hex()
        
    #     print(hex_hash)
        
    #     byte_hash = digest.fromhex(digest.hex())
        
    #     print(byte_hash)
        
    #     return byte_hash    
        
        # Do the same thing ^v
        
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256') 
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.user_password, password)
    
class LoginForm(FlaskForm):
    username = StringField("user_username", validators=[DataRequired()])
    password = PasswordField("user_password", validators=[DataRequired()])
    remember_me = BooleanField()


class RegisterForm(FlaskForm):
    username = StringField("user_username", validators=[DataRequired()])
    password = PasswordField("user_password", validators=[DataRequired()])
    firstName = StringField("user_firstName")
    lastName = StringField("user_lastName")
    
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    # email = StringField("email", validators=[DataRequired(), Email()])
    
# Add administrative views here
admin.add_view(ModelView(User, db.session))
admin.add_link(MenuLink(name='logout', category='', url="/"))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@app.route('/', methods = ['GET'])
def index():
    db.create_all()
    return render_template('login.html')

@app.route('/newUser', methods = ['GET'])
def newUser():
    return render_template('signup.html')

@app.route('/signup', methods = ['POST'])
def signup():
    form = RegisterForm(request.form)
    
    if request.method == 'POST':
        USERNAME = request.form.get('username')
        PASSWORD = request.form.get('pass')
        FIRSTNAME = request.form.get('firstName')
        LASTNAME = request.form.get('lastName')
        BIO = request.form.get('bio')
        
        USERTYPE = 'user'
        LASTCOLOR = 'black'
        
        conn = engine.connect()
        # print(PASSWORD)
        
        hashedPassword = User.set_password(User, PASSWORD)
        
        # print(hashedPassword)
        
        # query = text("SELECT user_Username FROM user WHERE user_Username = :s ")
        # # session.query(query, {"s": USERNAME})
        
        # findUsername = session.execute(query, {"s":USERNAME})
        # session.commit()
        
        # # print(type(findUsername.user_Username))
        # if findUsername == None :
        conn = engine.connect()
        # query2 = text("INSERT INTO user (user_Username, user_password, user_firstName, user_lastName, user_type, user_lastColor, user_bio) VALUES (:a, :b, :c, :d, :e, :f, :g) ")
        
        # newUser = session.execute(query2, {"a":USERNAME, "b": PASSWORD, "c": FIRSTNAME, "d": LASTNAME, "e": USERTYPE, "f":  LASTCOLOR, "g": BIO})
        newUser = User(id = 4, user_Username = USERNAME, user_password= PASSWORD, user_firstName=FIRSTNAME, user_lastName=LASTNAME, user_type=USERTYPE, user_lastColor=LASTCOLOR, user_Bio=BIO)
        # session.add(newUser)
        db.session.merge(newUser)
        session.commit()
        # session.close()
        
        
        gc.collect()
    
        return redirect(url_for('login'))
        
        # else:
        #     return "That username is already takem, please choose another"
            
    return "HELLOOOO"   #here we would put the link to register again
        
def toDict(students):
    resp={}
    for student in students:
        resp.update({student.student_name:student.enrollment_grade}) 
    return resp

@app.route('/login', methods = [ 'GET', 'POST'])
def login():
    USERNAME = request.form.get('username')
    PASSWORD = request.form.get('pass')
        
    if current_user.is_authenticated:
        return redirect(url_for('protected'))
    
    # form = LoginForm() 
    
    # if form.validate_on_submit():
        
    user = User.query.filter_by(user_Username = USERNAME).first()
    
    # print("Password as a string is: " + user.user_password)
    # print("Password as a string is: " + str(PASSWORD))
    # check = str(user.user_password) == str(PASSWORD)
    # print(check)

    if user and user.check_password(user.user_password):
        

        login_user(user)
        print(" unique")

        return redirect(url_for('protected'))

    
    else:
        print("not unique")
        # print("Password is: " + PASSWORD)
        # next = request.args.get('next')
        # # is_safe_url should check if the url is safe for redirects.
        # # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #     return abort(400)
        
        return "Bad Login"
    # print('didnt work')
    # return render_template('login.html')

# @app.route('/login', methods = [ 'POST'])
# def login():
#     USERNAME = request.form.get('username')
#     PASSWORD = request.form.get('pass')
        
#     if current_user.is_authenticated:
#         return redirect(url_for('protected'))
    
#     form = LoginForm() 
    
#     user = User.query.filter_by(user_Username = USERNAME, user_password = PASSWORD).first()
    
    
#     if existing_user:
#         login_user(user)
#         print(" unique")

#         return redirect(url_for('protected'))
    
        
#     else:
#         print("not unique")
#         # next = request.args.get('next')
#         # # is_safe_url should check if the url is safe for redirects.
#         # # See http://flask.pocoo.org/snippets/62/ for an example.
#         # if not is_safe_url(next):
#         #     return abort(400)
         
#         return "Bad Login"
        


@app.route('/protected')
@login_required
def protected():
    return 'logged in as: ' + current_user.user_Username



@app.route("/lobby", methods = ['GET', 'POST'])
@login_required
def lobby():
    return 'hello'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # return redirect(url_for('login'))
    return "Logged Out"


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'



# @login_manager.request_loader
# def request_loader(user_id):
#     # userID = request.form.get('email')
#     try:
#         return User.query.get(user_id)
#     except:
#         return None

@login_manager.user_loader 
def load_user(user_id): 
    return User.query.get(user_id)


 
    


if __name__ == '__app__':
    
    app.run(debug=True)
    
    
    #https://pythonprogramming.net/flask-registration-tutorial/