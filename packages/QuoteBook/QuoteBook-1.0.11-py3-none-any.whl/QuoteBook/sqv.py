# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../design/sqw.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Quote(object):
    def setupUi(self, Quote):
        Quote.setObjectName("Quote")
        Quote.resize(185, 66)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Quote.sizePolicy().hasHeightForWidth())
        Quote.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Quote)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lQuote = QtWidgets.QLabel(Quote)
        self.lQuote.setText("")
        self.lQuote.setObjectName("lQuote")
        self.verticalLayout.addWidget(self.lQuote)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lCharacter = QtWidgets.QLabel(Quote)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lCharacter.sizePolicy().hasHeightForWidth())
        self.lCharacter.setSizePolicy(sizePolicy)
        self.lCharacter.setText("")
        self.lCharacter.setObjectName("lCharacter")
        self.horizontalLayout.addWidget(self.lCharacter)
        self.lTitle = QtWidgets.QLabel(Quote)
        self.lTitle.setText("")
        self.lTitle.setObjectName("lTitle")
        self.horizontalLayout.addWidget(self.lTitle)
        self.lAuthor = QtWidgets.QLabel(Quote)
        self.lAuthor.setText("")
        self.lAuthor.setObjectName("lAuthor")
        self.horizontalLayout.addWidget(self.lAuthor)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnCopy = QtWidgets.QPushButton(Quote)
        self.btnCopy.setObjectName("btnCopy")
        self.horizontalLayout.addWidget(self.btnCopy)
        self.btnSQEdit = QtWidgets.QPushButton(Quote)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSQEdit.sizePolicy().hasHeightForWidth())
        self.btnSQEdit.setSizePolicy(sizePolicy)
        self.btnSQEdit.setObjectName("btnSQEdit")
        self.horizontalLayout.addWidget(self.btnSQEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Quote)
        QtCore.QMetaObject.connectSlotsByName(Quote)

    def retranslateUi(self, Quote):
        _translate = QtCore.QCoreApplication.translate
        Quote.setWindowTitle(_translate("Quote", "Quote"))
        self.btnCopy.setText(_translate("Quote", "Copy"))
        self.btnSQEdit.setText(_translate("Quote", "Edit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Quote = QtWidgets.QDialog()
    ui = Ui_Quote()
    ui.setupUi(Quote)
    Quote.show()
    sys.exit(app.exec_())

