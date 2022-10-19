from time import strptime
from flask import Flask, url_for, redirect, jsonify, request
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json, os
import sqlite3 as sql
from datetime import date, datetime
from sqlalchemy import text
from sqlalchemy.sql import func

myApp = Flask(__name__)
myApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carnappdb.sqlite'
myApp.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
db = SQLAlchemy(myApp)
ma = Marshmallow(myApp)

class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_username = db.Column(db.String(50), nullable=False)
    admin_password = db.Column(db.String(50), nullable=False)
    admin_logged_datetime = db.Column(db.String(50), nullable=False)

    def __init__(self, admin_username, admin_password, admin_logged_datetime):
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.admin_logged_datetime = admin_logged_datetime
        
        

class AdminSchema(ma.Schema):
    class Meta:
        fields = ("admin_id","admin_username", "admin_password", "admin_logged_datetime")

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50))
    user_logged_datetime = db.Column(db.String(50), nullable=False)

    def __init__(self, user_name, password, user_logged_datetime):
        self.user_name = user_name
        self.password = password
        self.user_logged_datetime = user_logged_datetime

class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "user_name", "password", "user_logged_datetime")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_logged_in = False

isAdmin_logged_in = False

USER = ""
ADMIN = ""

@myApp.route('/')
@myApp.route('/home')
def home():
    if (user_logged_in == True or isAdmin_logged_in == True):
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@myApp.route('/login')
def login():
    if (user_logged_in == True or isAdmin_logged_in == True):
        return redirect(url_for('home'))
    else:    
        return render_template('login.html')

@myApp.route('/register')
def register():
    if isAdmin_logged_in:
        return render_template('register.html')
    else:
        return redirect(url_for('home'))

@myApp.route('/submitlogin', methods=['GET', 'POST'])
def submitlogin():
    if request.method == 'POST':
        data = request.get_json()
        username = data[0]["username"]
        password = data[0]["password"]

        global user_logged_in, USER, isAdmin_logged_in, ADMIN

        admin_query = Admin.query.filter_by(admin_username=username).first()
        ADMIN = admin_schema.dump(admin_query)

        if(len(ADMIN)>0):
            if (ADMIN['admin_password'] == password):
                #return redirect(url_for("home")) 
                message = {'message':"Welcome"}

                isAdmin_logged_in = True
                

                admin = Admin.query.get(ADMIN['admin_id'])
                print(admin)
                curdatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                admin.admin_logged_datetime = str(curdatetime)

                db.session.commit()
                
                #return redirect(url_for('home'))
                

            else:
                ADMIN = None
                message = {'message':"Incorrect Email or Password"}
                #return redirect(url_for("test"))

        else:
            user_query = User.query.filter_by(user_name=username).first()
            USER = user_schema.dump(user_query)

            print(USER)
        
            message = ""
        
            if(len(USER)>0):
                if (USER['password'] == password):
                    #return redirect(url_for("home")) 
                    message = {'message':"Welcome"}

                    user_logged_in = True

                    user = User.query.get(USER['user_id'])
                    print(user)
                    curdatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    user.user_logged_datetime = str(curdatetime)

                    db.session.commit()

                    #return redirect(url_for('home'))

                else:
                    USER = None
                    message = {'message':"Incorrect Email or Password"}
                    #return redirect(url_for("test"))

            else:
                USER = None
                message = {'message':"There is no email registered"}
                #return redirect(url_for("test"))
        
    return jsonify(message)

@myApp.route('/createdAcc', methods=['GET', 'POST'])
def createdAcc():
    if request.method == 'POST':
        data = request.get_json()
        #print(data)

        username = data[0]['username']
        user_password = data[0]['password']
        curdatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        check_username = User.query.filter_by(user_name=username).first()
        existing_username = user_schema.dump(check_username)
        #print(len(existing_email))
        if len(existing_username) > 0:
            message = {'message':"Username is already used"}

        else:
            new_user = User(username, user_password, curdatetime)
            db.session.add(new_user)
            db.session.commit()

            message = {'message':"Successfully Registered"}
        
        return jsonify(message)

@myApp.route('/logout')
def logout():
    global user_logged_in, isAdmin_logged_in
    user_logged_in = False

    isAdmin_logged_in = False

    return redirect(url_for('login'))

if __name__ == "__main__":
    db.create_all()
    myApp.run(host="0.0.0.0", port=8080, debug=True)