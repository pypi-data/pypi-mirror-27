# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quotelistdesign.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(662, 594)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.quoteTree = QtWidgets.QTreeWidget(self.centralwidget)
        self.quoteTree.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.quoteTree.setAutoFillBackground(False)
        self.quoteTree.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.quoteTree.setAutoScrollMargin(16)
        self.quoteTree.setAlternatingRowColors(True)
        self.quoteTree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.quoteTree.setAutoExpandDelay(2)
        self.quoteTree.setIndentation(0)
        self.quoteTree.setUniformRowHeights(False)
        self.quoteTree.setAnimated(True)
        self.quoteTree.setAllColumnsShowFocus(True)
        self.quoteTree.setWordWrap(False)
        self.quoteTree.setHeaderHidden(False)
        self.quoteTree.setObjectName("quoteTree")
        self.quoteTree.header().setVisible(True)
        self.quoteTree.header().setCascadingSectionResizes(True)
        self.quoteTree.header().setDefaultSectionSize(200)
        self.quoteTree.header().setHighlightSections(True)
        self.quoteTree.header().setMinimumSectionSize(10)
        self.quoteTree.header().setSortIndicatorShown(False)
        self.quoteTree.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.quoteTree)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setObjectName("btnDelete")
        self.horizontalLayout_3.addWidget(self.btnDelete)
        self.btnEdit = QtWidgets.QPushButton(self.centralwidget)
        self.btnEdit.setObjectName("btnEdit")
        self.horizontalLayout_3.addWidget(self.btnEdit)
        self.btnNew = QtWidgets.QPushButton(self.centralwidget)
        self.btnNew.setObjectName("btnNew")
        self.horizontalLayout_3.addWidget(self.btnNew)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 662, 22))
        self.menuBar.setNativeMenuBar(True)
        self.menuBar.setObjectName("menuBar")
        self.menuSettings = QtWidgets.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menuBar)
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuSettings.addAction(self.actionPreferences)
        self.menuBar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QuoteBook"))
        self.quoteTree.setSortingEnabled(False)
        self.quoteTree.headerItem().setText(0, _translate("MainWindow", "Quote"))
        self.quoteTree.headerItem().setText(1, _translate("MainWindow", "Title"))
        self.quoteTree.headerItem().setText(2, _translate("MainWindow", "Category"))
        self.btnDelete.setText(_translate("MainWindow", "Delete"))
        self.btnEdit.setText(_translate("MainWindow", "Edit"))
        self.btnNew.setText(_translate("MainWindow", "New"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

