# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'child_gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(482, 366)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 320, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 21))
        self.label.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.label.setObjectName("label")
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(10, 40, 461, 261))
        self.tableView.setObjectName("tableView")
        self.roi_menu = QtWidgets.QComboBox(Dialog)
        self.roi_menu.setGeometry(QtCore.QRect(160, 10, 69, 22))
        self.roi_menu.setObjectName("roi_menu")
        self.show_img = QtWidgets.QPushButton(Dialog)
        self.show_img.setGeometry(QtCore.QRect(240, 10, 75, 23))
        self.show_img.setObjectName("show_img")

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Analysis Result:"))
        self.show_img.setText(_translate("Dialog", "查看图片"))

