DROPBOX CHECKING is a Flask app that scans a Dropbox folder in a given account, 
filters files that look like CVs (pdf, doc, docw, images... whose size is under 
8MB), and add them with their metadata to a Mongo database. The updates can be
seen in real time on the app.

HOW TO RUN IT:

	1- Sign in on Dropbox:
	[I give you login and password]
	Add your files ...

	2- In a first Terminal:
	$ cd [path to mongodb]/bin/
	$ sudo ./mongod

	3- In a second Terminal:
	$ cd [patth to the project]
	$ python app.py

	4- Then, open your favorite browser at url:
	http://127.0.0.1:5000/

You can add or delete files on the Dropbox account, the list in the app will be 
updated in real time.




