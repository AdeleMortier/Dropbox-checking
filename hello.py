from flask import Flask, request, session, g, redirect, url_for, abort, render_template, jsonify, flash
import os
import sqlite3
import db_to_mongo
app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_dbx()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

        

global dbx, mongo_coll

@section.before_request
def before_request():
	dbx = db_to_mongo.connect_dbx()
	mongo_coll = db_to_mongo.connect_mongo()

@app.route('/')
def update():
	return render_template('template.html')


@app.route('/refresh', methods= ['GET'])
def refreshData():
	"""dbx = db_to_mongo.connect_dbx()
	db, docs = db_to_mongo.connect_mongo()
	dbx_file_list = db_to_mongo.update_mongo_from_dbx(dbx, docs)"""
	mongo_file_list = fetch_mongo(mongo_coll)
	name_list = []
	date_list = []
	size_list = []
	for entry in dbx_file_list.keys():
		name_list.append(entry)
		date_list.append(dbx_file_list[entry][0])
		size_list.append(dbx_file_list[entry][1])

	return jsonify(names=name_list, dates=date_list, sizes=size_list)
	
if __name__ == '__main__':
    app.run(debug=True)