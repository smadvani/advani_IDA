# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FindDupLocations
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
 * 
 *                                                                         *
 * 2014-04-29: Transferred code from ...dialog.py to this file -to be able *
                   to use iface and follow standard QGIS plug in practice. *
               Added imports that were previously in ...dialog.py to this  *
                   as real work of the plug-in goes here.
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *

from PyQt4 import QtGui
from qgis.core import *
# Initialize Qt resources from file resources.py
import findduplocations_resources
# Import the code for the dialog
from findduplocationsdialog import FindDupLocationsDialog
import os.path
import sqlite3
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

class FindDupLocations:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'findduplocations_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = FindDupLocationsDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QtGui.QAction(
            QtGui.QIcon(":/plugins/findduplocations/icon.png"),
            u"Find Dup Locs", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Find Duplicate Locations", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Find Duplicate Locations", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        self.ui = self.dlg.ui
        self.get_databases()
        self.ui.pbRunQry.pressed.connect(self.dup_locs_sql)
        self.ui.pbClose.pressed.connect(self.close_fdl)
        #! Commented out below - templated from PluginBuilder - result never
        #!      equaled 1.
        # Run the dialog event loop
        ##result = self.dlg.exec_()
        # See if OK was pressed
        
        ##QtGui.QMessageBox.information(None,"result",str(result))
        ##if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
        ##self.iface = iface
            ##self.ui = self.dlg.Ui_FindDupLocations()
            ##self.get_databases()
            
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
        cur4.execute(sql4)self.ui.pbRunQry.pressed.connect(self.dup_locs_sql)
            self.ui.pbClose.pressed.connect(self.close_fdl)
        
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
        self.dlg.close()

