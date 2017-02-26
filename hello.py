from flask import Flask, request, session, g, redirect, url_for, abort, render_template, jsonify, flash
import threading
import time
import db_to_mongo
app = Flask(__name__)

def get_mongo():
    if not hasattr(g, 'mongo_db_collection'):
        g.mongo_db_collection = db_to_mongo.connect_mongo()
    return g.mongo_db_collection

def get_dbx():
    if not hasattr(g, 'dbx'):
        g.dbx = db_to_mongo.connect_dbx()
    return g.dbx

@app.before_first_request
def sync():
	mongo_collection = get_mongo()
	dbx = get_dbx()
	update_mongo_thread = threading.Thread(None, db_to_mongo.update_mongo_from_dbx, None, (dbx, mongo_collection), {}) 
	update_mongo_thread.start() 




@app.route('/')
def update():
	return render_template('template.html')

@app.route('/refresh', methods= ['GET'])
def refreshData():
	mongo_file_list = db_to_mongo.fetch_mongo(get_mongo())
	name_list = []
	date_list = []
	size_list = []
	for entry in mongo_file_list.keys():
		name_list.append(entry)
		date_list.append(mongo_file_list[entry][0])
		size_list.append(mongo_file_list[entry][1])
	return jsonify(names=name_list, dates=date_list, sizes=size_list)
	
if __name__ == '__main__':
    app.run(debug=True)