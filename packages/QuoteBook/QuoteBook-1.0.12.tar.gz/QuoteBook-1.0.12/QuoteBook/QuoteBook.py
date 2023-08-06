#!/usr/bin/env python3
import sys
import os
import json
import inspect

import pyperclip
from PyQt5 import QtCore, QtWidgets, QtGui

from .quotelistdesign import Ui_MainWindow
from .settingsdialog import Ui_Settings
from .sqv import Ui_Quote
from .editordialog import Ui_Editor


class Icon:
    @staticmethod
    def get():
        icon = QtGui.QIcon()
        icondir = os.path.join(os.path.dirname(inspect.getfile(QuoteBook)), "icon.ico")
        icon.addPixmap(QtGui.QPixmap(icondir), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        return icon

class Quote:
    def __init__(self):
        self.author = ""
        self.category = ""
        self.characters = ""
        self.date = ""
        self.quote = ""
        self.tags = ""
        self.title = ""

    def __str__(self):
        return str({'author': self.author, 'category': self.category, 'characters': self.characters, 'date': self.date,
                    'quote': self.quote, 'tags': self.tags, 'title': self.title})

    def setFromDict(self, dictionary):
        self.author = dictionary['author']
        self.category = dictionary['category']
        self.characters = dictionary['characters']
        self.date = dictionary['date']
        self.quote = dictionary['quote']
        self.tags = dictionary['tags']
        self.title = dictionary['title']

    def getAsDict(self):
        return {'author': self.author, 'category': self.category, 'characters': self.characters, 'date': self.date,
                'quote': self.quote, 'tags': self.tags, 'title': self.title}

    def copy(self):
        tmp = Quote()
        tmp.author = self.author
        tmp.category = self.category
        tmp.characters = self.characters
        tmp.date = self.date
        tmp.quote = self.quote
        tmp.tags = self.tags
        tmp.title = self.title
        return tmp

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.getAsDict() == other.getAsDict()


class QuoteFile:
    def __init__(self, filepath):
        self.path = os.path.join(filepath, "myQuotes.json")
        self.quotes = []
        if not self.exists():
            self.save()       # Creates empty quote file
        self.load()

    def save(self):
        quotesAsDict = []
        for quote in self.quotes:
            quotesAsDict.append(quote.getAsDict())
        with open(self.path, 'w') as File:
            json.dump(quotesAsDict, File)

    def exists(self):
        if not os.path.isfile(self.path):
            return 0
        else:
            return 1

    def load(self):
        self.quotes = []
        with open(self.path, 'r') as File:
            quotesAsDicts = json.load(File)
        for quoteAsDict in quotesAsDicts:
            quote = Quote()
            quote.setFromDict(quoteAsDict)
            self.quotes.append(quote)


class QuoteBook(Ui_MainWindow):
    def __init__(self, MainWindow):
        Ui_MainWindow.__init__(self)
        self.setupUi(MainWindow)
        MainWindow.setWindowIcon(Icon.get())
        self.mySettings = Settings.loadSettings()
        self.qf = QuoteFile(self.mySettings['dir'])
        self.selectedQuote = None
        self.btnNew.clicked.connect(self.makeQuote)
        self.quoteTree.itemSelectionChanged.connect(self.onSelect)
        self.btnEdit.clicked.connect(self.editQuote)
        self.btnDelete.clicked.connect(self.deleteQuote)
        self.actionPreferences.triggered.connect(self.settingsDialog)
        self.quoteTree.itemDoubleClicked.connect(self.SQView)
        self.showQuotes()

    def SQView(self):
        steve = SQV(self.SQI)
        steve.exec_()
        self.showQuotes()

    # Get selected quote's address and index
    def onSelect(self):
        self.selectedQuote = self.quoteTree.currentItem()
        for quote in self.qf.quotes:
            if quote.quote == self.selectedQuote.text(0):
                self.SQI = self.qf.quotes.index(quote)

    def deleteQuote(self):
        if self.selectedQuote is not None:
            self.qf.quotes.pop(self.SQI)
            self.qf.save()
            self.showQuotes()

    def editQuote(self):
        if self.selectedQuote:
            eddy = Editor(self.qf.quotes[self.SQI])
            eddy.exec_()
            self.qf.quotes[self.SQI] = eddy.getfinalquote()
            self.qf.save()
            self.showQuotes()

    def settingsDialog(self):
        setty = Settings()
        setty.exec_()

    def makeQuote(self):
        eddy = Editor(Quote())
        eddy.exec_()
        self.qf.quotes.append(eddy.getfinalquote())
        self.qf.save()
        self.showQuotes()

    # Show the quotes in the quoteTree
    def showQuotes(self):
        self.qf.load()
        self.quoteTree.setSortingEnabled(False)
        self.quoteTree.clear()
        for quote in self.qf.quotes:
            item_0 = QtWidgets.QTreeWidgetItem(self.quoteTree)
            self.quoteTree.topLevelItem(self.qf.quotes.index(quote)).setText(0, quote.quote)
            self.quoteTree.topLevelItem(self.qf.quotes.index(quote)).setText(1, quote.title)
            self.quoteTree.topLevelItem(self.qf.quotes.index(quote)).setText(2, quote.category)
        self.quoteTree.setSortingEnabled(True)
        if self.qf.quotes != []:
            self.quoteTree.topLevelItem(0).setSelected(False)
        self.quoteTree.setCurrentItem(None)
        self.selectedQuote = None


class SQV(QtWidgets.QDialog):
    def __init__(self, number):
        super(SQV, self).__init__()
        self.ui = Ui_Quote()
        self.ui.setupUi(self)
        self.setWindowIcon(Icon.get())
        self.SQI = number
        self.mySettings = Settings.loadSettings()
        self.qf = QuoteFile(self.mySettings['dir'])
        self.showQuote(self.SQI)
        self.ui.btnSQEdit.clicked.connect(self.editQuote)
        self.ui.btnCopy.clicked.connect(self.copyQuote)

    def copyQuote(self):
        pyperclip.copy(self.qf.quotes[self.SQI].quote)

    def editQuote(self):
            eddy = Editor(self.qf.quotes[self.SQI])
            eddy.exec_()
            self.qf.quotes[self.SQI] = eddy.getfinalquote()
            self.qf.save()
            self.showQuote(self.SQI)

    def showQuote(self, number):
        self.qf.load()
        self.ui.lQuote.setText('<html><head/><body><p align="justify">'
                               + '<span style=" font-style:italic;">"'
                               + self.qf.quotes[number].quote
                               + '"</span></p></body></html>')
        self.ui.lTitle.setText(self.qf.quotes[number].title)
        self.ui.lCharacter.setText(self.qf.quotes[number].characters)
        self.ui.lAuthor.setText(self.qf.quotes[number].author)


class Editor(QtWidgets.QDialog):
    def __init__(self, quote):
        super(Editor, self).__init__()
        self.ui = Ui_Editor()
        self.ui.setupUi(self)
        self.setWindowIcon(Icon.get())
        self.quote = quote
        self.oldquote = quote.copy()
        self.loadtext()
        self.ui.btnCancel.clicked.connect(self.cancel)
        self.ui.btnSave.clicked.connect(self.save)

    def cancel(self):
        self.savequote()
        if not self.waschanged():
            self.close()
        else:
            reply = QtWidgets.QMessageBox.question(
                None, QtCore.QCoreApplication.translate(
                    "Dialog", "Warning"),
                QtCore.QCoreApplication.translate(
                    "Dialog", "Do you want to save changes before leaving?"))
            if reply == QtWidgets.QMessageBox.No:
                self.close()
            else:
                self.save()

    def closeEvent(self, event):
        self.cancel()

    def save(self):
        self.savequote()
        self.oldquote = self.quote
        self.close()

    def savequote(self):
        self.quote.quote = self.ui.editQuote.toPlainText()
        self.quote.title = self.ui.editTitle.text()
        self.quote.category = self.ui.editCategory.text()
        self.quote.author = self.ui.editAuthor.text()
        self.quote.characters = self.ui.editCharacters.text()
        self.quote.date = self.ui.editDate.text()
        self.quote.tags = self.ui.editTags.text()

    def loadtext(self):
        self.ui.editQuote.setText(self.quote.quote)
        self.ui.editTitle.setText(self.quote.title)
        self.ui.editCategory.setText(self.quote.category)
        self.ui.editAuthor.setText(self.quote.author)
        self.ui.editCharacters.setText(self.quote.characters)
        self.ui.editDate.setText(self.quote.date)
        self.ui.editTags.setText(self.quote.tags)

    def waschanged(self):
        if self.quote == self.oldquote:
            return False
        else:
            return True

    def getfinalquote(self):
        return self.oldquote



class Settings(QtWidgets.QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowIcon(Icon.get())
        self.mySettings = self.loadSettings()
        self.setupSettings()
        self.ui.btnEdit.clicked.connect(self.directoryDialog)
        self.ui.btnCancel.clicked.connect(self.close)
        self.ui.btnApply.clicked.connect(self.saveSettings)

    @staticmethod
    def loadSettings():
        if os.path.isfile('./settings.json'):
            f = open('settings.json')
            mySettings = json.load(f)
            f.close()
        else:
            path = os.path.realpath('./')
            mySettings = {'dir': path}
        return mySettings

    def setupSettings(self):
        self.ui.directoryEdit.setText(self.mySettings['dir'])

    def saveSettings(self):
        olddir = self.mySettings['dir']
        newdir = self.ui.directoryEdit.text()
        os.makedirs(newdir, exist_ok=True)
        os.rename(os.path.join(olddir, "myQuotes.json"), os.path.join(newdir, "myQuotes.json"))
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
                                         QtCore.QCoreApplication.translate("Dialog", "Select Directory"),
                                         self.mySettings['dir'])
        self.ui.directoryEdit.setText(path)

def main():
    app = QtWidgets.QApplication(sys.argv)
    translator = QtCore.QTranslator()
    path = os.path.dirname(os.path.realpath(__file__))
    translator.load(QtCore.QLocale.system(), os.path.join(path, "QuoteBook_"))
    app.installTranslator(translator)
    MainWindow = QtWidgets.QMainWindow()
    prog = QuoteBook(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
