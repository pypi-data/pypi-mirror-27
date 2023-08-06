# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../design/settingsdialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(363, 82)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.directoryEdit = QtWidgets.QLineEdit(Dialog)
        self.directoryEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.directoryEdit.setObjectName("directoryEdit")
        self.horizontalLayout_2.addWidget(self.directoryEdit)
        self.btnEdit = QtWidgets.QPushButton(Dialog)
        self.btnEdit.setMaximumSize(QtCore.QSize(100, 25))
        self.btnEdit.setObjectName("btnEdit")
        self.horizontalLayout_2.addWidget(self.btnEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnApply = QtWidgets.QPushButton(Dialog)
        self.btnApply.setObjectName("btnApply")
        self.horizontalLayout.addWidget(self.btnApply)
        self.btnCancel = QtWidgets.QPushButton(Dialog)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Save directory</p></body></html>"))
        self.btnEdit.setText(_translate("Dialog", "Edit"))
        self.btnApply.setText(_translate("Dialog", "Apply"))
        self.btnCancel.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

