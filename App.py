#!/usr/bin/env python
#################################################
import sys
import time
import sqlite3
from flask import g
from flask import Flask, render_template, request
#################################################
# F.Roux, July 2019
##

# data-base client that runs in a web-browser to implement anotation system
# use as python App.py "/path/to/db/dbFile.db"

DATABASE = sys.argv[1] # database name

app = Flask(__name__) # initialize flask server

# connect client to db
def getDB():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# shutdown client-connection to db
@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# client route for main        
@app.route('/')
def main():
   return render_template('main.html')        

# client route for list
@app.route('/list',methods = ['POST', 'GET'])
def list():

   if (request.method == 'POST'):
      sIdx = request.form['StartIdx']# outer_start
      eIdx = request.form['EndIdx']# outer_end
      
   t = time.time()#start timer     
   db = getDB()
   db.row_factory = sqlite3.Row
   
   cur = db.cursor()
   
   #################################### 
   # query to extract exact matches   
   #################################### 
   sqlCmnd1 = """ SELECT orig_variant_id,outer_start,outer_end,copy_number_status,phenotype,data_origin FROM allSVNdat WHERE (outer_start == """+sIdx+""" AND outer_end == """+eIdx+""") AND (copy_number_status LIKE "%deletion%" OR copy_number_status LIKE "%duplication%" OR copy_number_status LIKE "%insertion%");""";

   ####################################
   # query to extract exact close hits
   #################################### 
   sqlCmnd2 = """ SELECT orig_variant_id,outer_start,outer_end,copy_number_status,phenotype,data_origin FROM allSVNdat WHERE ( ( (outer_start < """+sIdx+""" AND outer_end > """+eIdx+""") AND (inner_start >= """+sIdx+""" AND inner_end <= """+eIdx+""") ) OR ( ( (outer_start == """+sIdx+""" AND outer_end > """+eIdx+""") AND (inner_end <= """+eIdx+""") ) ) OR ( ( (outer_start < """+sIdx+""" AND outer_end == """+eIdx+""") AND (inner_start >= """+sIdx+""") ) ) ) AND (copy_number_status LIKE "%deletion%" OR copy_number_status LIKE "%duplication%" OR copy_number_status LIKE "%insertion%");""";

   # extract rows with exact matches
   cur = db.cursor()
   cur.execute( sqlCmnd1 )
   rows1 = cur.fetchall( ) # rows with exact matches

   # extract rows with close hits
   cur = db.cursor()
   cur.execute( sqlCmnd2 )
   rows2 = cur.fetchall( ) # rows with close hits

   print(time.time()-t)# query duration
   
   # route row data to list.html 
   return render_template("list.html",rows1 = rows1, rows2 = rows2)
   
if __name__ == '__main__':
   app.run(debug = True)
