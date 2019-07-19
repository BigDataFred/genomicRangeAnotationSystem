#!/usr/bin/env python
#################################################
import sqlite3
import re
#################################################
# F.Roux, July 2019
##
class db():
    
    
    def __init__(self):
        self=self
        
        
    def connectDB(self,dbName):
        db = sqlite3.connect(dbName)
        return db
        
        
    def createTable(self,db,tableName):        
        sqlcmd =  """ CREATE TABLE IF NOT EXISTS """+tableName+"""(unique_variant_id TEXT PRIMARY KEY,                                    
                                                outer_start INTEGER DEFAULT 0,
                                                start INTEGER DEFAULT 0,
                                                inner_start INTEGER DEFAULT 0,
                                                inner_end INTEGER DEFAULT 0,
                                                end INTEGER DEFAULT 0,
                                                outer_end INTEGER DEFAULT 0, 
                                                copy_number_status TEXT,
                                                orig_variant_id TEXT,
                                                data_origin TEXT,
                                                phenotype TEXT,
                                                UNIQUE(unique_variant_id)
                                                ); """

        c = db.cursor()
        c.execute(sqlcmd)
        

    def ceateRow(self,db,tableName,vals):        
        sqlcmd = """ INSERT INTO """+tableName+"""(unique_variant_id,                            
                            outer_start,
                            start,
                            inner_start,
                            inner_end,
                            end,
                            outer_end,
                            copy_number_status,
                            orig_variant_id,
                            data_origin,
                            phenotype) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?) """
                
        c = db.cursor()
        c.execute( sqlcmd, vals )
        return c.lastrowid           
        
        
    def createIndex4Table(self,db,tableName,optimCrit):
        sqlcmd = """ CREATE INDEX IF NOT EXISTS optimSearch4"""+tableName+""" ON """+tableName+""" """+optimCrit+"""; """
        c = db.cursor()
        c.execute( sqlcmd )
                      
        
    def extractStringIdx(self,patStr1, patStr2, stringDat):
        ix1 = re.search(patStr1,stringDat)
        ix2 = re.search(patStr2,stringDat[ix1.end():len(stringDat)])
        return ix1.end(),ix1.end()+ix2.start()
        
        
    def getChromosome(self,stringDat):
        chrom = int(re.search(r"(\d+)\.(\d+)",stringDat.split()[0]).groups()[0])
        return chrom
        
        
    def getMetDat(self,stringDat):
        metDat = stringDat[ re.search("ID=",stringDat).start():len(stringDat) ]
        return metDat
        
        
    def getUniqueVarID(self,stringDat):
       ix1,ix2 = self.extractStringIdx("ID=", ";", stringDat)
       uVarID  = stringDat[ix1:ix2]#variantID
       return uVarID
        
        
    def getOrigVarID(self,stringDat):
        ix1,ix2 = self.extractStringIdx("Name=", ";", stringDat)
        origVarID  = stringDat[ix1:ix2]#variantID
        return origVarID
        
        
    def getAlias(self,stringDat):
        ix1,ix2 = self.extractStringIdx("Alias=", ";", stringDat)
        alias  = stringDat[ix1:ix2]
        return alias
        
        
    def getSampleName(self,stringDat):
        try:
           ix1,ix2 = self.extractStringIdx("sample_name=", ";", stringDat)           
           sample = stringDat[ix1:ix2]
        except:
            sample = None
        return sample
        
        
    def getStartRange(self,stringDat):
        try:
            ix1,ix2 = self.extractStringIdx("Start_range=", ";", stringDat)     
            sR = re.search(r"(\d+)\,(\d+)",stringDat[ix1:ix2])
            if (len(sR) == 2):
                s = int(sR.groups()[1])#inner start
                iS = None
            else:
                if ( int( seR.groups()[1] ) < int( sR.groups()[2] ) ):
                   s = int( seR.groups()[1] )#start
                   iS = int( sR.groups()[2] )#inner start
                else:
                   s = int( seR.groups()[2] )#start
                   iS = int( sR.groups()[1] )#inner start
        except:
            s = None
            iS = None
        return s,iS
        
        
    def getStopRange(self,stringDat):
        try:
            ix1,ix2 = self.extractStringIdx("End_range=", ";", tmpDat)           
            eR = re.search(r"(\d+)\,(\d+)",stringDat[ix1:ix2])
            if (len(eR) == 2):
                e = int(eR.groups()[1])#inner end
                iE = None
            else:
                if ( int(eR.groups()[2]) > int(eR.groups()[1]) ):
                   e = int(eR.groups()[2])#end
                   iE = int(eR.groups()[1])#inner end
                else:
                   e = int(eR.groups()[1])#end
                   iE = int(eR.groups()[2])#inner end
        except:
            e = None
            iE = None
        return e,iE
        
        
    def getPhenotype(self,stringDat):
        try:
           ix1,ix2 = self.extractStringIdx("phenotype=", ";", stringDat)
           pheno  = stringDat[ix1:ix2]
        except:
            pheno = None
        return pheno
        
        
    def getDatOrigin(self,stringDat):
        try:
           ix1,ix2 = self.extractStringIdx("Dbxref=", ";", stringDat)
           datOrigin  = stringDat[ix1:ix2]
        except:
            datOrigin = None
        return datOrigin
            
        
    def dot2bar(self,x):
        m = re.finditer("\.",x)
        for tmp in m:
            l = list(x)
            l[tmp.start()]="_"
            x = "".join(l)
        return x
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
