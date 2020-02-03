from flask import Flask,request,jsonify,session
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from model import generate
import random
import string
import os

# instantiating the Flask class into app
app = Flask(__name__)

# instantiating the Api Class
api = Api(app)

# configurations 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "sqlite:///generate.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "ABCD 12345"


# instantiating the SQLAlchemy Class in db 
db=SQLAlchemy(app)

# this API is suppose to generate a random 
class generate_pin(Resource):

    def post(self):

        # the random funtion generates random 15 digits mixture of string and digits
        pin = ''.join([random.choice(string.digits) for n in range (15)])

        # creating a variable data and saving the value of the randomly generated pin
        data = generate(pin)

        # adding the pin to the database
        db.session.add(data)

        # commiting the new added item
        db.session.commit()

        # querying a column by the pin and saving it to the variable result
        result = generate.query.filter_by(pin = pin).first()
        
        # fetching the id of the particular pin and saving in s_N
        s_n = result.id
        return {'pin': pin, "SN":s_n }
        
 



api.add_resource(generate_pin, '/api/generate') 

class validate_pin(Resource):
    def post(self):
        # instantiating the request.get_json method to enable user to enter needed information
        request_data = request.get_json()

        # requesting a pin from user for validation
        pin = request_data['pin']
        SN = request_data['SN']

        # searching for that paticular pin in the database
        result1 = generate.query.filter_by(pin = pin).first()
        result2 = generate.query.filter_by(id = SN).first()
        
        # if pin is found it returns 1 for success
        if result1 == result2:
            return{"response":1}

        # else if pin is not found it returns o to represent failure
        else:
            return{"response": 0}    

api.add_resource(validate_pin, '/api/generate/validate')         
    




if  __name__ == "__main__":
    app.run(debug=True)