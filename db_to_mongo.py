import dropbox
import pymongo
import datetime
from pymongo import MongoClient
import hello

global allowed_extensions
allowed_extensions = ["pdf", "doc", "docx", "ppt", "pptx", "jpeg", "jpg", "png"]

def connect_dbx(): #connect to Dropbox
	dbx = dropbox.Dropbox('X__h8gWux9AAAAAAAAAAC7Z98TzfaS-LTRdml1SAxKOTiZAF40aikge1aOQihCLA')
	account_info = dbx.users_get_current_account()
	return dbx

def connect_mongo(): #connect toMongoDB
	client = MongoClient() #create MongoClient to the running monlgod instance
	mongo_db = client.mongo_db #create a database
	mongo_collection = mongo_db.mongo_collection #create a collection "mongo_coll"
	return mongo_collection

def fetch_mongo(mongo_collection):
	mongo_file_list = {}
	mongo_raw_file_list = mongo_collection.find()
	for doc in mongo_raw_file_list:
		mongo_file_list[doc["name"]] = [doc["date"], doc["size"]]
	print "before update: ", mongo_file_list
	return mongo_file_list

def fetch_dbx(dbx):
	dbx_raw_file_list = dbx.files_list_folder('/docs').entries #fetch all DB content
	dbx_file_list = {}
	for entry in dbx_raw_file_list:
		dbx_file_list[entry.name] = [entry.server_modified, entry.size]
	return dbx_file_list


def add_or_modify_mongo(dbx, mongo_collection, dbx_file_list, mongo_file_list):
	for entry_name in dbx_file_list.keys():
	#check if there are new files on Dropbox, filter them and add them to Mongo if needed
		entry_date = dbx_file_list[entry_name][0]
		entry_size = dbx_file_list[entry_name][1]

		if entry_name in mongo_file_list:
		#the file already exists in MongoDB
			if mongo_file_list[entry_name][0] != entry_date and entry_size <= 8000000:
			#the file has been modified since the last checkpoint, but has not become too big
				dbx.files_download_to_file(entry_name, "/docs/" + entry_name)
				mongo_collection.find_one_and_update({"name" : entry_name}, {'$inc' : {"size" : entry_size-mongo_file_list[entry_name][1]}, '$set' : {"date" : entry_date}})
		else:
		#the file does not exist in MongoDB
			entry_extension = entry_name[entry_name.rfind('.')+1:]
			if (entry_extension in allowed_extensions) and (entry_size <= 8000000):
			#test both filetype and size 
				dbx.files_download_to_file(entry_name, "/docs/" + entry_name)
				doc = {"name" : entry_name, "date" : entry_date, "size" : entry_size}
				mongo_collection.insert_one(doc)

def delete_mongo(mongo_collection, dbx_file_list, mongo_file_list):
	for mongo_entry_name in mongo_file_list.keys():
	#check if there are files on Mongo that have been deleted on Dropbox
		if mongo_entry_name not in dbx_file_list.keys():
			mongo_collection.delete_one({"name" : mongo_entry_name, "date" : mongo_file_list[mongo_entry_name][0], "size" : mongo_file_list[mongo_entry_name][1]})


def update_mongo_from_dbx(dbx, mongo_collection): #update MongoDB from Dropbox
	while 1:
		mongo_file_list = fetch_mongo(mongo_collection) #dictionnary of the form dict[name] = [date, size]
		dbx_file_list = fetch_dbx(dbx) #dictionnary of the form dict[name] = [date, size]
		add_or_modify_mongo(dbx, mongo_collection, dbx_file_list, mongo_file_list)
		delete_mongo(mongo_collection, dbx_file_list, mongo_file_list)








	
