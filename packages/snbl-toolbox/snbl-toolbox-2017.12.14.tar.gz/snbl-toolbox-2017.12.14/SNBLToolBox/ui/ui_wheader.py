# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SNBLToolBox/ui/ui_wheader.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WHeader(object):
    def setupUi(self, WHeader):
        WHeader.setObjectName("WHeader")
        WHeader.resize(521, 421)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/header"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        WHeader.setWindowIcon(icon)
        WHeader.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtWidgets.QVBoxLayout(WHeader)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(WHeader)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.folderLineEdit = QtWidgets.QLineEdit(WHeader)
        self.folderLineEdit.setObjectName("folderLineEdit")
        self.horizontalLayout.addWidget(self.folderLineEdit)
        self.folderButton = QtWidgets.QToolButton(WHeader)
        self.folderButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/folder"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folderButton.setIcon(icon1)
        self.folderButton.setObjectName("folderButton")
        self.horizontalLayout.addWidget(self.folderButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.valuesList = QtWidgets.QListWidget(WHeader)
        self.valuesList.setObjectName("valuesList")
        self.verticalLayout.addWidget(self.valuesList)
        self.resultTable = QtWidgets.QTableWidget(WHeader)
        self.resultTable.setObjectName("resultTable")
        self.resultTable.setColumnCount(0)
        self.resultTable.setRowCount(0)
        self.verticalLayout.addWidget(self.resultTable)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.runButton = QtWidgets.QPushButton(WHeader)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/run"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.runButton.setIcon(icon2)
        self.runButton.setObjectName("runButton")
        self.horizontalLayout_2.addWidget(self.runButton)
        self.stopButton = QtWidgets.QPushButton(WHeader)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/stop"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(icon3)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_2.addWidget(self.stopButton)
        self.saveButton = QtWidgets.QPushButton(WHeader)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/save"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon4)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.runProgressBar = QtWidgets.QProgressBar(WHeader)
        self.runProgressBar.setProperty("value", 0)
        self.runProgressBar.setObjectName("runProgressBar")
        self.horizontalLayout_2.addWidget(self.runProgressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(WHeader)
        QtCore.QMetaObject.connectSlotsByName(WHeader)

    def retranslateUi(self, WHeader):
        _translate = QtCore.QCoreApplication.translate
        WHeader.setWindowTitle(_translate("WHeader", "Header Extractor"))
        self.label.setText(_translate("WHeader", "Folder"))
        self.runButton.setText(_translate("WHeader", "Run"))
        self.stopButton.setText(_translate("WHeader", "Stop"))
        self.saveButton.setText(_translate("WHeader", "Save text"))

from . import resources_rc
