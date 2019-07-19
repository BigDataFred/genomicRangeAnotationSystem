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
        if (ix1!=None):
            ix2 = re.search(patStr2,stringDat[ix1.end():len(stringDat)])        
            return ix1.end(),ix1.end()+ix2.start()
        else:
            return 0, 0
        
        
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
        ix1,ix2 = self.extractStringIdx("Start_range=", ";", stringDat)
        if ( (ix1 != 0) & (ix2 != 0) ):      
            sR = re.search(r"(\d+)\,(\d+)",stringDat[ix1:ix2])
            if (sR != None):
                if (len(sR.groups()) == 2):
                    if ( int( sR.groups()[0] ) < int( sR.groups()[1] ) ):
                        s = int( sR.groups()[0] )#start
                        iS = int( sR.groups()[1] )#inner start
                    else:
                        s = int( sR.groups()[1] )#start
                        iS = int( sR.groups()[0] )#inner start
                else:
                    s = int(sR.groups()[0])#inner start
                    iS = None
            else:
                s = None
                iS = None
        else:
            s = None
            iS = None
        return s,iS
        
        
    def getStopRange(self,stringDat):
        ix1,ix2 = self.extractStringIdx("End_range=", ";", stringDat)    
        if ( (ix1 != 0) & (ix2 != 0) ):       
            eR = re.search(r"(\d+)\,(\d+)",stringDat[ix1:ix2])
            if (eR != None):
                if (len(eR.groups()) == 2):
                    if ( int(eR.groups()[1]) > int(eR.groups()[0]) ):
                        e = int(eR.groups()[1])#end
                        iE = int(eR.groups()[0])#inner end
                    else:
                        e = int(eR.groups()[0])#end
                        iE = int(eR.groups()[1])#inner end
                else:
                    e = int(eR.groups()[1])#inner end
                    iE = None
            else:
                e = None
                iE = None
        else:
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
