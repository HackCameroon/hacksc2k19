import smartcar
from flask import url_for, Flask, redirect, request, jsonify
from flask_cors import CORS
import pyrebase
import json
import datetime

import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None
email = None
dic = None

config = {
          "apiKey": "AIzaSyDHbigP1k14RMRi7UJCg6EpS3TELNdTOeg",
          "authDomain": "hacksc2019.firebaseapp.com",
          "databaseURL": "https://hacksc2019.firebaseio.com",
          "storageBucket": "hacksc2019.appspot.com",
        }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('bhagatv@uci.edu', 'admin123')
db = firebase.database()

client = smartcar.AuthClient(
    client_id = "db0c47e9-4ab8-45d1-be16-2e474625279a",
    client_secret = "98588318-38af-4b62-b5de-7139609561eb",
    redirect_uri = 'http://0.0.0.0:80/exchange',
    scope=['read_vehicle_info','control_security', 'control_security:unlock', 'control_security:lock','read_location','read_odometer',],
    test_mode=False
)



@app.route('/login', methods=['GET', 'POST'])
def login():
    global email 
    email = request.args.get('email')
    email = email.replace('.','__dot__')
    auth_url = client.get_auth_url()
    print(auth_url + '&lol=12')
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')
    
    # access our global variable and store our access tokens
    global access
    global email
    global dic
    
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    access['expiration'] = str(access['expiration'])
    access['refresh_expiration'] = str(access['refresh_expiration'])

    #dic = {email:access}
    return redirect('/vehicle')


@app.route('/vehicle', methods=['GET'])
def vehicle():
    # access our global variable to retrieve our access tokens
    global access
    global email
    global dic
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    vehicle_info = vehicle.info()
    vehicle_id = vehicle_info['id']
    del vehicle_info['id']
    dic = {email : {'ids' : {vehicle_id : True}}}
    db.child("User").child(email).child('cars_owned').child('ids').update({vehicle_id : True})
    
    dic = {vehicle_id:{}}
    
    dic[vehicle_id]['access'] = access
    dic[vehicle_id]['info'] = vehicle_info
    dic[vehicle_id]['location'] = vehicle.location()
    dic[vehicle_id]['odometer'] = vehicle.odometer()
    dic[vehicle_id]['odometer']['age'] = str(dic[vehicle_id]['odometer']['age'])
    dic[vehicle_id]['location']['age'] = str(dic[vehicle_id]['location']['age'])
    dic[vehicle_id]['rented'] = False
    #dic[email]['ids'][vehicle_id].update(access)

    print(vehicle.location())
    print(vehicle.odometer())
    db.child("Car").child(vehicle_id).set(dic[vehicle_id])
    #db.child("Renter").child("test").push("LOL")
    info = vehicle.info()
    print(info)

    return jsonify(info)

@app.route('/rent', methods=['GET'])
def rent():
    vehicle_id = request.args.get('id')
    email = request.args.get('email').replace('.','__dot__')
    if not db.child('Car').child(vehicle_id).get().val()['rented']:
        db.child('Car').child(vehicle_id).update({'rented' : True})
        db.child('User').child(email).child('cars_rented').child('ids').update({vehicle_id : True})
        return jsonify({'status':'Success'})
    else:
        return jsonify({'status':'Error, car already rented out.'})

@app.route('/client_login', methods = ['GET','POST'])
def client_login():
    if request.method == 'POST':
        data = request.form
        user = data['user'].replace('.','__dot__')
        password = data['password']
        if db.child('User').child(user).get().val()['password'] == password:
            return jsonify({'status':'Success'})
        else:
            return jsonify({'status':'Error, wrong password'})


@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.form
        user = data['user'].replace('.','__dot__')
        password = data['password']
        db.child('User').child(user).child('password').set(password)
        db.child('User').child(user).child('cars_owned').child('ids').set({})
        db.child('User').child(user).child('cars_rented').child('ids').set({})
        return jsonify({'status':'Success'})


@app.route('/unlock', methods = ['GET','POST'])
def unlock():
    if request.method == 'POST':
        data = request.form
        email = data['email'].replace('.','__dot__')
        vehicle_id = data['vehicle_id']

        cars_rented = db.child('User').child(email).child('cars_rented').child('ids').get().val()
        if vehicle_id in cars_rented and cars_rented[vehicle_id]:
            vehicle_access = db.child('Car').child(vehicle_id).child('access').get().val()['refresh_token']

            new_access = client.exchange_refresh_token(vehicle_access)
            new_access['expiration'] = str(new_access['expiration'])
            new_access['refresh_expiration'] = str(new_access['refresh_expiration'])
            db.child('Car').child(vehicle_id).child('access').set(new_access)
            vehicle = smartcar.Vehicle(vehicle_id, new_access['access_token'])
            #vehicle.unlock()
            return jsonify({'status':'Success'})
        else:
            return jsonify({'status':'You do not have access to this vehicle.'})

@app.route('/lock', methods = ['GET','POST'])
def lock():
    if request.method == 'POST':
        data = request.form
        email = data['email'].replace('.','__dot__')
        vehicle_id = data['vehicle_id']

        cars_rented = db.child('User').child(email).child('cars_rented').child('ids').get().val()
        if vehicle_id in cars_rented and cars_rented[vehicle_id]:
            vehicle_access = db.child('Car').child(vehicle_id).child('access').get().val()['refresh_token']

            new_access = client.exchange_refresh_token(vehicle_access)
            new_access['expiration'] = str(new_access['expiration'])
            new_access['refresh_expiration'] = str(new_access['refresh_expiration'])
            db.child('Car').child(vehicle_id).child('access').set(new_access)
            vehicle = smartcar.Vehicle(vehicle_id, new_access['access_token'])
            vehicle.lock()
            return jsonify({'status':'Success'})
        else:
            return jsonify({'status':'You do not have access to this vehicle.'})








if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 80)
