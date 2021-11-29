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

app = Flask(__name__, static_url_path='', static_folder='')
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

# metadata_ob.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(100), unique = True, nullable = False)
    user_password = db.Column(db.String(100), nullable = False)
    user_type = db.Column(db.Text, nullable = False)
    user_lastColor = db.Column(db.Text, nullable = False)
    user_Bio = db.Column(db.Text, nullable = True)

    def __init__ (self, user_id, user_name, user_password, user_type, user_lastColor, user_Bio):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password
        self.user_type = user_type
        self.user_lastColor = user_lastColor
        self.user_Bio = user_Bio
        
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
    
    
    
# Add administrative views here
admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Teacher, db.session))
# admin.add_view(ModelView(Student, db.session))
# admin.add_view(ModelView(Courses, db.session))
# admin.add_view(ModelView(Enrollment, db.session))
# admin.add_link(MenuLink(name='logout', category='', url="/"))


@login_manager.user_loader 
def load_user(user_id): 
    try:
        return User.query.get(user_id)
    except:
        return None

@app.route('/', methods = ['GET'])
def startPage():
    db.create_all()

    return render_template('login.html')


if __name__ == '__app__':
    
    app.run(debug=True)