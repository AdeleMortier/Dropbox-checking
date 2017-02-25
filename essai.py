#! /usr/bin/python
# -*- coding:utf-8 -*-
import dropbox
from flask import Flask
app = Flask(__name__)

@app.route('/')
def connect_dbx():
	dbx = dropbox.Dropbox('X__h8gWux9AAAAAAAAAAC7Z98TzfaS-LTRdml1SAxKOTiZAF40aikge1aOQihCLA')
	account_info = dbx.users_get_current_account()
	return "Connection done!"

def check_dbx():
	allowed_extensions = ["pdf", "doc", "docx", "ppt", "pptx", "jpeg", "jpg", "png"]
	while true:
		file_list = dbx.files_list_folder('/docs').entries

		for entry in file_list:
			entry_size = entry.size
			entry_name = entry.name
			entry_extension = entry_name[entry_name.rfind('.')+1:]

			if (entry_extension in allowed_extensions) and (entry_size <= 8000000): 
				dbx.files_download_to_file(entry_name, "/docs/" + entry_name)
	return "check ok"


if __name__ == '__main__':
    app.run(debug=True)
