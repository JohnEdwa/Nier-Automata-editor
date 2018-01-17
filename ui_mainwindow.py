# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName("mainwindow")
        mainwindow.resize(445, 294)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        mainwindow.setFont(font)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(mainwindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(mainwindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.gameDataHeaderLabel = QtWidgets.QLabel(mainwindow)
        self.gameDataHeaderLabel.setText("")
        self.gameDataHeaderLabel.setObjectName("gameDataHeaderLabel")
        self.horizontalLayout.addWidget(self.gameDataHeaderLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gamesaveslotLayout = QtWidgets.QVBoxLayout()
        self.gamesaveslotLayout.setObjectName("gamesaveslotLayout")
        self.verticalLayout.addLayout(self.gamesaveslotLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "NieR;Automata Save Editor"))
        self.label.setText(_translate("mainwindow", "GameData.dat header: "))

