# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editordialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Editor(object):
    def setupUi(self, Editor):
        Editor.setObjectName("Editor")
        Editor.resize(400, 349)
        self.gridLayout = QtWidgets.QGridLayout(Editor)
        self.gridLayout.setObjectName("gridLayout")
        self.editCategory = QtWidgets.QLineEdit(Editor)
        self.editCategory.setObjectName("editCategory")
        self.gridLayout.addWidget(self.editCategory, 2, 1, 1, 1)
        self.editTitle = QtWidgets.QLineEdit(Editor)
        self.editTitle.setObjectName("editTitle")
        self.gridLayout.addWidget(self.editTitle, 1, 1, 1, 1)
        self.editQuote = QtWidgets.QTextEdit(Editor)
        self.editQuote.setObjectName("editQuote")
        self.gridLayout.addWidget(self.editQuote, 0, 1, 1, 1)
        self.editAuthor = QtWidgets.QLineEdit(Editor)
        self.editAuthor.setObjectName("editAuthor")
        self.gridLayout.addWidget(self.editAuthor, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(Editor)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btnSave = QtWidgets.QPushButton(Editor)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_6.addWidget(self.btnSave)
        self.btnCancel = QtWidgets.QPushButton(Editor)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_6.addWidget(self.btnCancel)
        self.gridLayout.addLayout(self.horizontalLayout_6, 7, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Editor)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        self.editCharacters = QtWidgets.QLineEdit(Editor)
        self.editCharacters.setObjectName("editCharacters")
        self.gridLayout.addWidget(self.editCharacters, 4, 1, 1, 1)
        self.editDate = QtWidgets.QLineEdit(Editor)
        self.editDate.setObjectName("editDate")
        self.gridLayout.addWidget(self.editDate, 5, 1, 1, 1)
        self.editTags = QtWidgets.QLineEdit(Editor)
        self.editTags.setObjectName("editTags")
        self.gridLayout.addWidget(self.editTags, 6, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Editor)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_4 = QtWidgets.QLabel(Editor)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_5 = QtWidgets.QLabel(Editor)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_6 = QtWidgets.QLabel(Editor)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_7 = QtWidgets.QLabel(Editor)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Editor)
        QtCore.QMetaObject.connectSlotsByName(Editor)

    def retranslateUi(self, Editor):
        _translate = QtCore.QCoreApplication.translate
        Editor.setWindowTitle(_translate("Editor", "QuoteEdit"))
        self.label.setText(_translate("Editor", "Quote"))
        self.btnSave.setText(_translate("Editor", "Save"))
        self.btnCancel.setText(_translate("Editor", "Cancel"))
        self.label_2.setText(_translate("Editor", "Title"))
        self.label_3.setText(_translate("Editor", "Category"))
        self.label_4.setText(_translate("Editor", "Author"))
        self.label_5.setText(_translate("Editor", "Characters"))
        self.label_6.setText(_translate("Editor", "Date"))
        self.label_7.setText(_translate("Editor", "Tags"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Editor = QtWidgets.QDialog()
    ui = Ui_Editor()
    ui.setupUi(Editor)
    Editor.show()
    sys.exit(app.exec_())

