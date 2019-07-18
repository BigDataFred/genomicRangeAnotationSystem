#!/usr/bin/env python
#################################################
import sys
import os
import re
import time
from dbTools import db
#################################################
# F.Roux, July 2019
##

def loadGVFdb(p2gvf,gvfName,savePath,chromNr=1):
    
    #This function loads chromosome specific gvf data into an sqlite database
    #p2f: path to file
    #fName: file name
    #savePath: path to save resulting .db file 
    #chromNr: chromosome number (e.g. 1) for which data should be extracted
    
    snvDB = db()# initialize db
    con = snvDB.connectDB(savePath+"snvDB.db")# connect to sqlite db
    print( con )
    tableName = "allSVNdat" #.dot2bar(gvfName)#change dots to underscores #
    
    snvDB.createTable(con,tableName)#create new table in db 
    snvDB.createIndex4Table(con,tableName,"(outer_start,outer_end)") # optimizing search queries to match t = O*(log n)
        
    print("reading "+p2gvf+gvfName)
    print("#########################")

    t = time.time()#start timer
    f= open(p2gvf+gvfName,'r')#start reading gvf file 

    cnt = 0
    rowCnt = 0
    for line in f:# there are 36,358,083 lines
        cnt+=1# increment counter
        if (cnt>10):#skip header
        
             tmpDat = line
             #print(tmpDat)
             
             #get chromosome of snv
             chrom = snvDB.getChromosome( tmpDat )
             if ( chrom == chromNr ):                                  
                 
                 #meta data
                 metDat = snvDB.getMetDat( tmpDat )
                 
                 #unique variant identifier
                 uVarID  = snvDB.getUniqueVarID( tmpDat )
                 
                 #original variant identifier
                 origVarID  = snvDB.getOrigVarID( tmpDat )
                 
                 #start range
                 s,iS = snvDB.getStartRange( tmpDat )
                 
                 #stop range
                 e,iE = snvDB.getStopRange( tmpDat )
                 
                 #data origin
                 datOrigin = snvDB.getDatOrigin( tmpDat )
                 
                 #phenotype
                 pheno  = snvDB.getPhenotype( tmpDat )
                 
                 #prepare the snv-data that will be added to table
                 tmpDat = tmpDat.split()
                 
                 uVarID = uVarID+origVarID+tmpDat[3]+tmpDat[4]+tmpDat[2]
                 
                 vals = ( uVarID, tmpDat[3], s, iS, iE, e, tmpDat[4], tmpDat[2], origVarID, datOrigin, pheno )   
                 
                 #create a new snv entry in the table
                 try:
                    rowCnt+=1#keep track of number of rows processed
                    tmp = snvDB.ceateRow(con,tableName,vals)
                 except:
                     print( "WARNING:"+uVarID+" is not unique" )
                     
    con.commit()#commit changes to db
    f.close()#close file    
    print(str(rowCnt)+"/"+str(cnt))#count number of snvs that were processed in total
    print(time.time()-t)#measure elapsed time
    print("#########################")
