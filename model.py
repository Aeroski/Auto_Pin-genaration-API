from flask_sqlalchemy import SQLAlchemy
from flask import(Flask,Blueprint,render_template,redirect,request,flash,url_for,session,logging)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///generate.sqlite3"
db=SQLAlchemy(app)

class generate(db.Model):
    id = db.Column('serial_number', db.Integer, primary_key=True)
    pin = db.Column(db.String(50))
   


    def __init__(self, pin):
        self.pin = pin
       

        db.create_all()