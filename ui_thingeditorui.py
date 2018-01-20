# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thingeditorui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ThingsManager(object):
    def setupUi(self, ThingsManager):
        ThingsManager.setObjectName("ThingsManager")
        ThingsManager.resize(611, 390)
        ThingsManager.setWindowTitle("")
        ThingsManager.setModal(False)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(ThingsManager)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.table = QtWidgets.QTableView(ThingsManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.table.setObjectName("table")
        self.horizontalLayout_2.addWidget(self.table)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ThingsManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.saveButton = QtWidgets.QPushButton(ThingsManager)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton)
        self.closeButton = QtWidgets.QPushButton(ThingsManager)
        self.closeButton.setObjectName("closeButton")
        self.verticalLayout.addWidget(self.closeButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(ThingsManager)
        QtCore.QMetaObject.connectSlotsByName(ThingsManager)

    def retranslateUi(self, ThingsManager):
        _translate = QtCore.QCoreApplication.translate
        self.saveButton.setText(_translate("ThingsManager", "Save"))
        self.closeButton.setText(_translate("ThingsManager", "Close"))

