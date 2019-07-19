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

# use as python App.py "/path/to/db/"

app = Flask(__name__)

p2db = sys.argv[1]
print(p2db)
DATABASE = p2db+'snvDB.db'

def getDB():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
@app.route('/')
def main():
   return render_template('main.html')        

@app.route('/list',methods = ['POST', 'GET'])
def list():

   if (request.method == 'POST'):
      sIdx = request.form['StartIdx']
      eIdx = request.form['EndIdx']
      sMode = request.form['start']
      eMode = request.form['end']
      
   print("start-index:"+sIdx)
   print("start-index:"+eIdx)
   print("start-mode:"+sMode)
   print("end-mode:"+eMode)
      
   t = time.time()#start timer     
   db = getDB()
   db.row_factory = sqlite3.Row
   
   cur = db.cursor()
   #sqlCmnd1 = "SELECT name FROM sqlite_master WHERE type IN ('table') AND name NOT LIKE 'sqlite_%';"   
   #tables = cur.execute( sqlCmnd1 ) 
   
   #cntTbl = 0
   #tbl = []
   #for tmp in tables:
    #   tbl.append(tmp[0])
    #   cntTbl+=1
   #print(tbl)
   
   #sqlCmnd2 = ""
   #cnt = 0
   #for tmp in tbl:
      #if (cnt <cntTbl-1):    
         #sqlCmnd2 = sqlCmnd2+" SELECT orig_variant_id,outer_start,outer_end,copy_number_status,phenotype,data_origin FROM "+tmp+" WHERE "+sMode+">= "+sIdx+" AND "+eMode+"<= "+eIdx+" UNION";
      #else:
         #sqlCmnd2 = sqlCmnd2+" SELECT orig_variant_id,outer_start,outer_end,copy_number_status,phenotype,data_origin FROM "+tmp+" WHERE "+sMode+">= "+sIdx+" AND "+eMode+"<= "+eIdx+";";                        
      #cnt+=1
      
   sqlCmnd2 = """ SELECT orig_variant_id,outer_start,outer_end,copy_number_status,phenotype,data_origin FROM allSVNdat WHERE ("""+sMode+"""== """+sIdx+""" AND """+eMode+"""== """+eIdx+""") AND (copy_number_status == "deletion" OR copy_number_status == "duplication" OR copy_number_status == "insertion");""";
   print(sqlCmnd2)
   cur = db.cursor()
   cur.execute( sqlCmnd2 )
   rows = cur.fetchall( )
   print(time.time()-t)
   
   return render_template("list.html",rows = rows, rows2 = rows)
   
if __name__ == '__main__':
   app.run(debug = True)
