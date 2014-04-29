# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_findduplocations.ui'
#
# Created: Thu Apr 10 10:36:06 2014
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FindDupLocations(object):
    def setupUi(self, FindDupLocations):
        FindDupLocations.setObjectName(_fromUtf8("FindDupLocations"))
        FindDupLocations.resize(1038, 536)
        FindDupLocations.setToolTip(_fromUtf8(""))
        self.lblFindDupLocs = QtGui.QLabel(FindDupLocations)
        self.lblFindDupLocs.setGeometry(QtCore.QRect(10, 10, 301, 71))
        self.lblFindDupLocs.setObjectName(_fromUtf8("lblFindDupLocs"))
        self.pbClose = QtGui.QPushButton(FindDupLocations)
        self.pbClose.setGeometry(QtCore.QRect(894, 482, 91, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pbClose.setFont(font)
        self.pbClose.setObjectName(_fromUtf8("pbClose"))
        self.lblChoosePrjct = QtGui.QLabel(FindDupLocations)
        self.lblChoosePrjct.setGeometry(QtCore.QRect(50, 90, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblChoosePrjct.setFont(font)
        self.lblChoosePrjct.setObjectName(_fromUtf8("lblChoosePrjct"))
        self.cbxChoosePrjct = QtGui.QComboBox(FindDupLocations)
        self.cbxChoosePrjct.setGeometry(QtCore.QRect(10, 120, 191, 21))
        self.cbxChoosePrjct.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.cbxChoosePrjct.setObjectName(_fromUtf8("cbxChoosePrjct"))
        self.lstListLocations = QtGui.QListWidget(FindDupLocations)
        self.lstListLocations.setGeometry(QtCore.QRect(10, 240, 631, 231))
        self.lstListLocations.setLineWidth(100)
        self.lstListLocations.setAlternatingRowColors(True)
        self.lstListLocations.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.lstListLocations.setObjectName(_fromUtf8("lstListLocations"))
        self.pbRunQry = QtGui.QPushButton(FindDupLocations)
        self.pbRunQry.setGeometry(QtCore.QRect(10, 160, 131, 41))
        self.pbRunQry.setObjectName(_fromUtf8("pbRunQry"))
        self.pbShowLocs = QtGui.QPushButton(FindDupLocations)
        self.pbShowLocs.setGeometry(QtCore.QRect(540, 480, 101, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pbShowLocs.setFont(font)
        self.pbShowLocs.setToolTip(_fromUtf8(""))
        self.pbShowLocs.setObjectName(_fromUtf8("pbShowLocs"))
        self.lblChoosePrjct_2 = QtGui.QLabel(FindDupLocations)
        self.lblChoosePrjct_2.setGeometry(QtCore.QRect(10, 210, 631, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblChoosePrjct_2.setFont(font)
        self.lblChoosePrjct_2.setObjectName(_fromUtf8("lblChoosePrjct_2"))
        self.spxAdjPrecision = QtGui.QSpinBox(FindDupLocations)
        self.spxAdjPrecision.setGeometry(QtCore.QRect(340, 170, 41, 21))
        self.spxAdjPrecision.setToolTip(_fromUtf8(""))
        self.spxAdjPrecision.setMaximum(6)
        self.spxAdjPrecision.setProperty("value", 4)
        self.spxAdjPrecision.setObjectName(_fromUtf8("spxAdjPrecision"))
        self.lblAdjPrecision = QtGui.QLabel(FindDupLocations)
        self.lblAdjPrecision.setGeometry(QtCore.QRect(180, 170, 151, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblAdjPrecision.setFont(font)
        self.lblAdjPrecision.setObjectName(_fromUtf8("lblAdjPrecision"))

        self.retranslateUi(FindDupLocations)
        QtCore.QMetaObject.connectSlotsByName(FindDupLocations)

    def retranslateUi(self, FindDupLocations):
        FindDupLocations.setWindowTitle(QtGui.QApplication.translate("FindDupLocations", "FindDupLocations", None, QtGui.QApplication.UnicodeUTF8))
        self.lblFindDupLocs.setText(QtGui.QApplication.translate("FindDupLocations", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Find Duplicate Location Codes</span></p><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Copyright © 2014 Integral Consulting</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pbClose.setText(QtGui.QApplication.translate("FindDupLocations", "Close Form", None, QtGui.QApplication.UnicodeUTF8))
        self.lblChoosePrjct.setText(QtGui.QApplication.translate("FindDupLocations", "Choose Project", None, QtGui.QApplication.UnicodeUTF8))
        self.pbRunQry.setText(QtGui.QApplication.translate("FindDupLocations", "Find Duplicate Locations", None, QtGui.QApplication.UnicodeUTF8))
        self.pbShowLocs.setText(QtGui.QApplication.translate("FindDupLocations", "Show In Project", None, QtGui.QApplication.UnicodeUTF8))
        self.lblChoosePrjct_2.setText(QtGui.QApplication.translate("FindDupLocations", "<html><head/><body><p align=\"center\">List of Duplicate Locations</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lblAdjPrecision.setText(QtGui.QApplication.translate("FindDupLocations", "<html><head/><body><p align=\"right\">Round X/Y Precision</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

