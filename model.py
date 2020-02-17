from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,session
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///generate.sqlite3"
db=SQLAlchemy(app)
migrate = Migrate(app,db)

class generate(db.Model):
    id = db.Column('user id', db.Integer, primary_key=True)
    # serial_number = db.Column(db.String(100))
    pin = db.Column(db.String(50))
    def __init__(self,pin):
        # self.serial_number = serial_number
        self.pin = pin

        db.create_all()