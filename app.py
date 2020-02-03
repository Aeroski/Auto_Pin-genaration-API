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

#homepage
class index(Resource):
    def get(self):

        return jsonify({"message": "add /api/generate to the route to generate pin",
        "message2":" add /api/generate/validate/<string:sn> to the route to validate pin"})
    

api.add_resource(index, '/')       

# this API is suppose to generate a random 
class generate_pin(Resource):

    def get (self):

        # the random funtion generates random 15 digits
        pin = ''.join([random.choice(string.digits) for n in range (15)])

        # the random funtion generates random 15 digits mixture of string and digits as serial number
        serial_number = ''.join([random.choice(string.ascii_letters+string.digits)for i in range(12)])
        



        # creating a variable data and saving the value of the randomly generated pin and serial number
        data = generate(serial_number,pin)

        # adding the pin and serial_number to the database
        db.session.add(data)

        # commiting the new added items
        db.session.commit()

        # querying a column by the pin and saving it to the variable result
        result = generate.query.filter_by(pin = pin).first()
        
        # fetching the id of the particular pin and saving in s_N
        s_n = result.serial_number
        return {'pin': pin, "SN":s_n }
        
 



api.add_resource(generate_pin, '/api/generate') 

class validate_pin(Resource):
    def get(self,sn):
       
        # searching for that paticular serial number in the database
        result = generate.query.filter_by(serial_number = sn).first()
        
        # if serial number is found it returns 1 for success
        if result:
            return{"response":1}

        # else if pin is not found it returns o to represent failure
        else:
            return{"response": 0}    

api.add_resource(validate_pin, '/api/generate/validate/<string:sn>')         
    




if  __name__ == "__main__":
    app.run(debug=True)