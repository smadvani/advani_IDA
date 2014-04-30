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
               dup_locs_sql                                                *
 * 2014-04-29  Removed all code below self.ui.setupUi(self) and placed in  *
               findduplocations.py
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


