# CommunityBoard
Communitive Whiteboard Webapp for CSE 106

To create a virtual environment, run the appropriate command in your terminal. (Note our team developed on VSCode)
For more info, we referred to this site: **https://code.visualstudio.com/docs/python/tutorial-flask**

# Linux
sudo apt-get install python3-venv    # If needed
python3 -m venv .venv
source .venv/bin/activate

# macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
py -3 -m venv .venv
.venv\scripts\activate

# Installing Packages

To install all required packages, once you have activated your virtual environment make sure to navigate into your working folder. Once inside the folder, within the terminal run command 

pip install -r requirements.txt

# Databases

There are two different databases that we use with our project.

--SQLite

This is used as our main development database since it runs what we need to do our testing. For this, within app.py make sure that the lines that contain the following are   **UNCOMMENTED**:
  ```
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
  engine = create_engine('sqlite:///app.db', echo = True)
  ```

--mysql

This is an example that is used in our main deployed webpage. To test against a mysql database follow these steps:

  -Make sure the following is **UNCOMMENTED**
  ```
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@localhost/newDB'
  engine = create_engine('mysql+pymysql://root:0000@localhost/newDB', echo = True)
  ```
Next, you must uncomment the follow code block

 @app.before_first_request
 
 ```
 def create_user():

     db.create_all()
     
     hashedPassword = generate_password_hash('00')
     
     user_datastore.creainte_user(email='admin@admin.com', username = 'admin', password= hashedPassword)
     
     db_session.commit()
     
     db_session.close()
  ```

   The above will create the db table that holds any column that are indicated in each respective ORM Table creation.
   
   Then run turn on the Flask server by using command: python3 -m flask run
   
   You may exit out of the Flask server to confirm your db is created.
