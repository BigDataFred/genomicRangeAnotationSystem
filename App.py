#!/usr/bin/env python
#################################################
import sqlite3
from flask import g
from flask import Flask, render_template, request
#################################################
# F.Roux, July 2019
##
app = Flask(__name__)

DATABASE = '/Users/froux/Desktop/genAnotationSys/snvDB.db'

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
      oS = request.form['OuterStart']
      oE = request.form['OuterEnd']
   print(oS)
   print(oE)         
   db = getDB()
   db.row_factory = sqlite3.Row
   
   cur = db.cursor()
   
   rows = db.execute(" SELECT variant_id,copy_number_status,phenotype FROM GRCh37_variant_call_gvf WHERE outer_start> "+oS+" AND outer_start < "+oE+"; ");
   print(rows)
   return render_template("list.html",rows = rows)
   
if __name__ == '__main__':
   app.run(debug = True)