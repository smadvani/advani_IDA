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
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load FindDupLocations class from file FindDupLocations
    from findduplocations import FindDupLocations
    return FindDupLocations(iface)
