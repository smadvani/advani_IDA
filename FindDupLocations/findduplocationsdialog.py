# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FindDupLocationsDialog
                                 A QGIS plugin
 Find coordinates for which there are multiple location codes and fix
                             -------------------
        begin                : 2014-03-13
        copyright            : (C) 2014 by Sanjay Advani/ Integral Consulting Inc.
        email                : sadvani@integral-corp.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 * 2014-03-14: start by importing same classes as imported in EDM - in add-*
               ition to PyQt4 imports given by plug-in builder. SA.        *
 * 2014-03-17: add  get_databases and dup_locs_sql functions as building   *
               blocks to functions to connect to db and run SQL to find    *
               duplicates. SA.    
 * 2014-04-01  Created first version that writes a list of location codes  *
               with their respective X/Y coordinates that are replicated.  *
               Next: clean up the list and be able to map it.  SA.         *
 * 2014-04-08  Copied bin/FindDupLocations and all contents to             * 
               C:\Program Files\Quantum GIS Lisboa\bin\FindDupLocations    *
               as this was originally created with the directory pathways  *
               and db table names for idba 1.8.  Changed for IDA2.0 with   *
               tables named ida_ instead of idba_ and directory for pro-   *
               ject files = iDAnalyst\ instead of iDBanalyst\              *
 * 2014-04-10  IDA db names are changed - changed how curDb is defined in  *
               dup_locs_sql
 ***************************************************************************/
"""

from PyQt4 import QtCore
from PyQt4 import QtGui
from qgis.core import *

import os
import sqlite3
import psycopg2
import datetime
import io
import math

import shutil

import ogr
import numpy as np
from shapely.geometry import *

# for extracting data from excel files
import xlrd

from xml.dom.minidom import parseString
from ui_findduplocations import Ui_FindDupLocations
# create the dialog for zoom to point


class FindDupLocationsDialog(QtGui.QDialog, Ui_FindDupLocations):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.ui = Ui_FindDupLocations()        
        self.ui.setupUi(self)
        #self.iface = iface
        self.get_databases()
        self.ui.pbRunQry.pressed.connect(self.dup_locs_sql)        
        self.ui.pbClose.pressed.connect(self.close_fdl)
        #.pressed.connect(self.close_edm)
        
 #Create functions to run query to find duplocations       
    def get_databases(self):
        '''
        Connect to a project database
        '''
        global curDb
        global curPrjName
        # get list of IDBA projects from folder names
        dList = []
        dList = os.listdir('C:\iDAnalyst\projects')
        self.ui.cbxChoosePrjct.clear()
        for dnm in dList:
            dstr = "C:\\iDAnalyst\\projects\\" + dnm
            if os.path.isdir(dstr):
                self.ui.cbxChoosePrjct.addItem(dnm)
                

    def dup_locs_sql(self):
        '''
        Connect to selected database and run SQL to find 
        unique x/y with multiple location codes
        ### Consider using script - and excutescript see http://www.pythoncentral.io/advanced-sqlite-usage-in-python/ ###
        '''
               
        global curDb
        global curPrjName
        curPrjName = str(self.ui.cbxChoosePrjct.currentText())
        ##QtGui.QMessageBox.information(None,"Current Project",curPrjName)
        curDb = '' 
        curDb = "C:\\iDAnalyst\\projects\\"+curPrjName+"\\db\\"+curPrjName+"_ida.db"
        ##QtGui.QMessageBox.information(None,"Current Database",curDb)
        CrdPrec = self.ui.spxAdjPrecision.value() 
        con = sqlite3.connect(curDb)
        sql = "drop VIEW if exists main.UNQ_loc_coord;"
        cur = con.cursor()
        cur.execute(sql)
        prec = str(CrdPrec)
        sql2 = "create VIEW main.UNQ_loc_coord as " \
        + " select distinct location, ROUND(X,"+prec+") as Xcoord, ROUND(Y,"+prec+") as Ycoord from ida_allresults;"
        cur2 = con.cursor()
        cur2.execute(sql2)
        
        sql3 = "drop VIEW if exists main.UNQ_coord_cnt;"
        cur3 = con.cursor()
        cur3.execute(sql3)
        
        sql4 = "CREATE VIEW main.UNQ_coord_cnt as " \
        + " SELECT distinct Xcoord, Ycoord, count(location) from UNQ_loc_coord" \
        + " GROUP BY Xcoord, Ycoord" \
        + " HAVING count(location)>1 ;"
        cur4 = con.cursor()
        cur4.execute(sql4)
        
        sql5 = "drop VIEW if exists main.DupLocCodes;"
        cur5 = con.cursor()
        cur5.execute(sql5)
        
        sql6 = "CREATE VIEW main.DupLocCodes as " \
        + " SELECT DISTINCT ar.location, ar.X, ar.Y " \
        + " FROM ida_allresults as ar INNER JOIN UNQ_coord_cnt as vw on ar.X = vw.Xcoord and ar.Y = vw.Ycoord ORDER BY X, Y, location;"
        cur6 = con.cursor()
        cur6.execute(sql6)
        
        sql7 = "select * from DupLocCodes" \
        + " ORDER BY X, Y, location ;"
        cur7 = con.cursor()
        cur7.execute(sql7)
        dup_locs_lst = cur7.fetchall()
        #con.close()
        #QtGui.QMessageBox.information(None,"CheckSQL", str(dup_locs_lst))
        
        locs = []
        for f in dup_locs_lst:
            locs.append(str(f[0]))
        
        if len(locs) == 0:
            QtGui.QMessageBox.information(None,"No duplicate locations", "All unique pairs of" \
                    + " X/Y coordinates at the selected level of precision are associated with unique location identifiers.")
        else:
            sql8 = "select count(*) from UNQ_coord_cnt"
            cur8 = con.cursor()
            cur8.execute(sql8)
            UnqXY = str(cur8.fetchone()[0])
            QtGui.QMessageBox.information(None,"Number of Unique X/Y", "There are "+UnqXY+" unique XY pairs with more than 1 location code associated" \
                    + " with them.  Please review to determine if these associations are correct.")
            #LIST RESULTS IN lstListLocations
            self.ui.lstListLocations.clear()
            for rec in dup_locs_lst:
                loc = rec[0]
                Xcoord = rec[1] 
                Ycoord = rec[2]
                pad1 = '%'+str(40-len(loc))+'s'
                pad2 = '%-'+str(40-len(str(Xcoord)))+'s'
                ##QtGui.QMessageBox.information(None,"length", "Pad1= "+pad1+"; Pad2= "+pad2)
                #! 2014-04-02: create  20-length of string pad to be able to left justify all at the same place in list box. 
                self.ui.lstListLocations.addItem(str(loc) + '%20s' %  str(Xcoord)+ '%20s' % str(Ycoord))  
                ##self.ui.lstListLocations.addItem(str(loc) + pad1 %  str(Xcoord) + pad2 % str(Ycoord))                
                #QtGui.QMessageBox.information(None,"CheckSQL", str(dup_locs_lst))
            
        con.close()
    
    def close_fdl(self):
        #self.write_fldmap_definition_file()
        self.ui.lstListLocations.clear()
        self.close()
