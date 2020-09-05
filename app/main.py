from flask import Flask
from flask import request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from json import loads, dumps
import os

FIREBASE_CFG = {}
FIREBASE_CFG[ "projectId" ] = "fasterclass-f83ac"
FIREBASE_CFG[ "databaseURL" ] = "https://fasterclass-f83ac.firebaseio.com"

credential = credentials.Certificate( os.environ.get( "GOOGLE_APPLICATION_CREDENTIALS" ) )

firebase_admin.initialize_app( credential, FIREBASE_CFG )

app = Flask(__name__)

@app.route("/")
def home_view():
	return dumps( db.reference( "/" ).get() )

@app.route("/seed")
def hash():
	args = request.args
	seed = "git seed"
	if args:
		coords = (args["lat"], args["long"])
		seed = -1
		if coords:
			new_coords = get_geocode_coords(coords)
			seed = hash_coords(new_coords)
		print(seed)
	return f"<h1>{seed}</h1>"

