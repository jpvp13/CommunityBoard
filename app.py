from flask import Flask, redirect, url_for, request,render_template, json, flash
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login.utils import login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import url,create_engine
from sqlalchemy.orm import session, sessionmaker, relationship
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user,login_manager, LoginManager
from sqlalchemy.sql.schema import MetaData
from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy import Table, Column, Integer, String, MetatData, ForeignKey
from sqlalchemy.sql import text
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


app = Flask(__name__, static_url_path='', static_folder='')
# app.config.from_object('config')
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
engine = create_engine('sqlite:///app.db', echo = True)
# # set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Course Information', template_mode='bootstrap3')
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

login_manager = LoginManager() 
login_manager.init_app(app) 
login_manager.login_view = 'login'

db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# metadata_ob.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_Username = db.Column(db.String(100), unique = True, nullable = False)
    user_password = db.Column(db.String(100), nullable = False)
    user_firstName = db.Column(db.String(100), nullable = False)
    user_lastName = db.Column(db.String(100), nullable = False)
    user_type = db.Column(db.Text, nullable = False)
    user_lastColor = db.Column(db.Text, nullable = False)
    user_Bio = db.Column(db.Text, nullable = True)

    def __init__ (self, user_id, user_name, user_password, user_type, user_lastColor, user_Bio,user_firstName,user_lastName):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = generate_password_hash(user_password)
        self.user_type = user_type
        self.user_lastColor = user_lastColor
        self.user_Bio = user_Bio
        self.user_lastName = user_lastName
        self.user_firstName = user_firstName
        
    def __repre__(self):
        return self.user_name
    
    def is_authenticated(self):
        return True
        # return None

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(user_id):         
        return str(user_id)
    
    def check_password(self, password):
        return check_password_hash(4, password)
    
class LoginForm(FlaskForm):
    username = StringField("user_username", validators=[DataRequired()])
    password = PasswordField("user_password", validators=[DataRequired()])
    remember_me = BooleanField()


class RegisterForm(FlaskForm):
    username = StringField("user_username", validators=[DataRequired()])
    password = PasswordField("user_password", validators=[DataRequired()])
    firstName = StringField("user_firstName")
    lastName = StringField("user_lastName")

    # email = StringField("email", validators=[DataRequired(), Email()])
    
# Add administrative views here
admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Teacher, db.session))
# admin.add_view(ModelView(Student, db.session))
# admin.add_view(ModelView(Courses, db.session))
# admin.add_view(ModelView(Enrollment, db.session))
admin.add_link(MenuLink(name='logout', category='', url="/"))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    # USERNAME = request.form.get('username')
    # PASSWORD = request.form.get('pass')

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            login_user(user)
            flash("User Athenticated!")
        else:
            flash("Login Invalid!")
    else:
        print(form.errors)

    return render_template('login.html', form=form)
# @app.route('/login', methods = ['POST'])
# def authUser():
    
    
#     USERNAME = request.form.get('username')
#     PASSWORD = request.form.get('pass')
    
#     user = User.query.filter_by(user_name = USERNAME, user_password = PASSWORD).first() 
#     # userType = user.user_type
#     # print(userType)
#     if current_user.is_authenticated: 
#         # return redirect(url_for('/views'))
        
#         differentViews(user)
#         # return redirect('/views/user')
    
#     if request.method == "POST":
        
#         if user is None or user.user_password != PASSWORD: 
#             # flash(u"Username or Password is invalid!", 'error')
#             return "<p>The username or password entered is invalid!</p>" 
#         else:   #!here we will add the password check with hashing for later proj
#             login_user(user)
#             # return redirect('/views/user')
#             return differentViews(user)
        
        
        
#     # return redirect(url_for('.index'))
#         # print("inside of existing")
#     return render_template('login.html')


# @login_required
# def differentViews(user):
    
#     if user.user_type == "user":
#         return "user"
#     elif user.user_type == "Admin":
#         return redirect('admin')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    username = form.username.data
    password = form.password.data
    firstName = form.firstName.data
    lastName = form.lastName.data
    # email = form.email.data
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username, password, firstName, lastName)
            db.session.add(user)
            db.session.commit()

        # return redirect(url_for('login'))
        return render_template('lobby.html')

    else:
        
        #!enter any message to inform user to try again
        return render_template('signup.html', form=form)

@app.route("/lobby", methods = ['GET', 'POST'])
@login_required
def lobby():
    return 'hello'


@app.route('/logout')
def logout():
    logout_user()
    # return redirect(url_for('login'))
    return "Logged Out"


@login_manager.user_loader 
def load_user(user_id): 
    try:
        return User.query.get(user_id)
    except:
        return None

@app.route('/', methods = ['GET'])
def login():
    db.create_all()

    return render_template('login.html')


if __name__ == '__app__':
    
    app.run(debug=True)