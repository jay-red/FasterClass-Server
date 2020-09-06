from flask import Flask
from flask import Response
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from json import loads, dumps
import os

FIREBASE_CFG = {}
FIREBASE_CFG[ "projectId" ] = "fasterclass-f83ac"
FIREBASE_CFG[ "databaseURL" ] = "https://fasterclass-f83ac.firebaseio.com"

credential = credentials.Certificate( loads( os.environ.get( "GOOGLE_APPLICATION_CREDENTIALS" ) ) )

firebase_admin.initialize_app( credential, FIREBASE_CFG )

LESSONS = {}

app = Flask(__name__)

@app.route( "/" )
def home_view():
	return ""

@app.route( "/code/<uid>/<lesson>/<file_name>.<ext>" )
def get_file( uid = None, lesson = None, file_name = None, ext = None ):
	print(uid, lesson, file_name, ext)
	if uid and lesson and file_name and ext:
		ref = db.reference( "/code/" + uid + "/" + lesson + "/" + file_name + ext )
		f = ref.get()
		resp = None
		if f:
			resp = Response( f )
			resp.headers[ "Access-Control-Allow-Origin" ] = "*"
		else:
			resp = Response("/* Not found. */")
			resp.headers[ "Access-Control-Allow-Origin" ] = "*"
		ext = ext.lower()
		if ext == "js":
			resp.headers[ "content-type" ] = "application/javascript; charset=utf-8"
		elif ext == "css":
			resp.headers[ "content-type" ] = "text/css; charset=utf-8"
		return resp
	else:
		resp = Response("/* Not found. */")
		resp.headers[ "Access-Control-Allow-Origin" ] = "*"
		return resp