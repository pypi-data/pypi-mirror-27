#!/usr/bin/env python3
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import pprint
from settingsdialog import Ui_Dialog
import json
_translate = QtCore.QCoreApplication.translate

class Settings(QtWidgets.QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.mySettings = self.loadSettings()
        self.setupSettings()
        self.ui.btnEdit.clicked.connect(self.directoryDialog)
        self.ui.btnCancel.clicked.connect(self.close)
        self.ui.btnApply.clicked.connect(self.saveSettings)
    def loadSettings(self):
        if os.path.isfile('./settings.json'):
            f = open('settings.json')
            mySettings = json.load(f)
            f.close()
        else:
            path = os.path.realpath('./')
            mySettings = {'dir':path}
        return mySettings
    def setupSettings(self):
        self.ui.directoryEdit.setText(self.mySettings['dir'])
    def saveSettings(self):
        olddir = self.mySettings['dir']
        newdir = self.ui.directoryEdit.text()
        os.makedirs(newdir, exist_ok=True)
        os.rename(os.path.join(olddir, "myQuotes.json"), os.path.join(newdir,
            "myQuotes.json"))
        self.mySettings['dir'] = newdir
        f = open('settings.json', 'w')
        json.dump(self.mySettings, f)
        f.close()
    def directoryDialog(self):
        print("Wybor sciezki")
        okno = QtWidgets.QFileDialog(self)
        okno.setFileMode(2)
        okno.setOption(okno.ShowDirsOnly, True)
        path = okno.getExistingDirectory(self,
        _translate("Dialog","Select Directory"),
        self.mySettings['dir'])
        self.ui.directoryEdit.setText(path)
def main():
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    prog = Settings(0)
    Dialog.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
