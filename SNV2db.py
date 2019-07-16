#!/usr/bin/env python
#################################################
import sys
import os
import re
import time
from dbTools import db
#################################################
# F.Roux, June 2019
##

def loadGVFdb(p2gvf,gvfName,chromNr=1):
    
    #This function loads chromosome specific gvf data into an sqlite database
    #p2f: path to file
    #fName: file name
    #chromNr: chromosome number (e.g. 1) for which data should be extracted
    
    snvDB = db()# initialize db
    con = snvDB.connectDB("/Users/froux/Desktop/genAnotationSys/snvDB.db")# connect to sqlite db
    tableName = snvDB.dot2bar(gvfName)#change dots to underscores
    print("creating table " +tableName)
    snvDB.createTable(con,tableName)#create new table in db

    print("reading "+p2gvf+gvfName)
    print("#########################")

    t = time.time()#start timer
    f= open(p2gvf+gvfName,'r')#start reading gvf file 

    cnt = 0
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
                 
                 #variantID
                 varID  = snvDB.getVarID( tmpDat )
                 
                 #variant alias
                 alias  = snvDB.getAlias( tmpDat )
                 
                 # variant sample
                 sample = snvDB.getSampleName( tmpDat )
                 
                 #start range
                 s,iS = snvDB.getStartRange( tmpDat )
                 
                 #stop range
                 e,iE = snvDB.getStopRange( tmpDat )
                 
                 #phenotype
                 pheno  = snvDB.getPhenotype( tmpDat )
                 
                 #prepare the snv-data that will be added to table
                 tmpDat = tmpDat.split()
                 vals = ( varID, alias, sample, tmpDat[0], tmpDat[3], s, iS, iE, e, tmpDat[4], tmpDat[2], pheno, metDat )   
                 
                 #create a new snv entry in the table
                 try:
                     tmp = snvDB.ceateRow(con,tableName,vals)
                 except:
                     print(vals)
            
                #if (cnt>100):
                #    break

    con.commit()#commit changes to db
    f.close()#close file    
    print(cnt)#count number of snvs that were processed in total
    print(time.time()-t)#measure elapsed time
    print("#########################")
