import sys
import re
import os
from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.originalFileNames = []
        self.newFileNames = []
        self.initUI()

    def initUI(self):
        #Use QT Designer code to create the ui
        self.setupUi(self)

        #Connect buttons
        self.folderBtn.clicked.connect(self.selectFolder)
        self.runBtn.clicked.connect(self.rename)
        self.folderPath.editingFinished.connect(self.generateSearchFileNames)
        self.searchFilePatternText.textChanged.connect(self.generateSearchFileNames)
        self.fileExtension.textChanged.connect(self.generateSearchFileNames)
        self.fileExtensionCheck.stateChanged.connect(self.generateSearchFileNames)
        self.newFilePatternText.textChanged.connect(self.generateNewFileNamesPreview)

        self.setWindowTitle('File Renamer')
        self.show()

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(300, 389)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.folderBtn = QtGui.QPushButton(Form)
        self.folderBtn.setObjectName(_fromUtf8("folderBtn"))
        self.gridLayout.addWidget(self.folderBtn, 0, 0, 1, 1)
        self.newFilePatternLabel = QtGui.QLabel(Form)
        self.newFilePatternLabel.setObjectName(_fromUtf8("newFilePatternLabel"))
        self.gridLayout.addWidget(self.newFilePatternLabel, 1, 2, 1, 1)
        self.searchFilePatternLabel = QtGui.QLabel(Form)
        self.searchFilePatternLabel.setObjectName(_fromUtf8("searchFilePatternLabel"))
        self.gridLayout.addWidget(self.searchFilePatternLabel, 1, 0, 1, 1)
        self.originalFileNamesLabel = QtGui.QLabel(Form)
        self.originalFileNamesLabel.setObjectName(_fromUtf8("originalFileNamesLabel"))
        self.gridLayout.addWidget(self.originalFileNamesLabel, 3, 0, 1, 1)
        self.searchFilePatternText = QtGui.QLineEdit(Form)
        self.searchFilePatternText.setObjectName(_fromUtf8("searchFilePatternText"))
        self.gridLayout.addWidget(self.searchFilePatternText, 2, 0, 1, 1)
        self.folderPath = QtGui.QLineEdit(Form)
        self.folderPath.setObjectName(_fromUtf8("folderPath"))
        self.gridLayout.addWidget(self.folderPath, 0, 2, 1, 1)
        self.newFileNamesList = QtGui.QListView(Form)
        self.newFileNamesList.setObjectName(_fromUtf8("newFileNamesList"))
        self.gridLayout.addWidget(self.newFileNamesList, 4, 2, 1, 1)
        self.originalFileNamesList = QtGui.QListView(Form)
        self.originalFileNamesList.setObjectName(_fromUtf8("originalFileNamesList"))
        self.gridLayout.addWidget(self.originalFileNamesList, 4, 0, 1, 1)
        self.fileExtensionCheck = QtGui.QCheckBox(Form)
        self.fileExtensionCheck.setObjectName(_fromUtf8("fileExtensionCheck"))
        self.gridLayout.addWidget(self.fileExtensionCheck, 5, 2, 1, 1)
        self.runBtn = QtGui.QPushButton(Form)
        self.runBtn.setObjectName(_fromUtf8("runBtn"))
        self.gridLayout.addWidget(self.runBtn, 7, 0, 1, 1)
        self.newFileNamesLabel = QtGui.QLabel(Form)
        self.newFileNamesLabel.setObjectName(_fromUtf8("newFileNamesLabel"))
        self.gridLayout.addWidget(self.newFileNamesLabel, 3, 2, 1, 1)
        self.newFilePatternText = QtGui.QLineEdit(Form)
        self.newFilePatternText.setObjectName(_fromUtf8("newFilePatternText"))
        self.gridLayout.addWidget(self.newFilePatternText, 2, 2, 1, 1)
        self.fileExtension = QtGui.QLineEdit(Form)
        self.fileExtension.setObjectName(_fromUtf8("fileExtension"))
        self.gridLayout.addWidget(self.fileExtension, 5, 0, 1, 1)
        self.fileExtensionCheck.toggle()
        self.fileExtension.setText(".txt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "File Renamer", None))
        self.folderBtn.setText(_translate("Form", "Select Folder", None))
        self.newFilePatternLabel.setText(_translate("Form", "Substitute String", None))
        self.searchFilePatternLabel.setText(_translate("Form", "Search File Pattern", None))
        self.originalFileNamesLabel.setText(_translate("Form", "Original File Names", None))
        self.fileExtensionCheck.setText(_translate("Form", "Specific Extension", None))
        self.runBtn.setText(_translate("Form", "Rename", None))
        self.newFileNamesLabel.setText(_translate("Form", "New File Names", None))

    #Dialog for getting folder path
    def selectFolder(self):
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.folderPath.setText(file)
        self.generateSearchFileNames()

    def generateSearchFileNames(self):

        if os.path.isdir(self.folderPath.text()) :
            os.chdir(self.folderPath.text())
        else :
            reply = QtGui.QMessageBox.warning(self, 'Message',
                                               "This Folder Does Not Exist!", QtGui.QMessageBox.Ok,
                                               QtGui.QMessageBox.Ok)
            self.folderPath.setText("")
            return


        #Get all files in the folder with the right extension
        if self.fileExtensionCheck.isChecked() :
            listFiles = [f for f in os.listdir(self.folderPath.text()) if os.path.splitext(f)[1] == self.fileExtension.text()]
        else :
            listFiles = [f for f in os.listdir(self.folderPath.text())]

        #Only use file names that match the pattern
        self.originalFileNames.clear()
        for f in listFiles :
            fName, fExtension = os.path.splitext(f)
            if re.search(self.searchFilePatternText.text(), fName, flags=re.I) :
                 self.originalFileNames.append(f)


        #Add file names to the QListView
        model = QtGui.QStandardItemModel()
        for f in self.originalFileNames:
            item = QtGui.QStandardItem(f)
            model.appendRow(item)
        self.originalFileNamesList.setModel(model)

        #Generate new preview
        self.generateNewFileNamesPreview()

    def generateNewFileNamesPreview(self):
        self.newFileNames.clear()
        for f in self.originalFileNames:
            fName, fExtension =  os.path.splitext(f)
            fName = re.sub(self.searchFilePatternText.text(), self.newFilePatternText.text(),fName, flags=re.I)
            self.newFileNames.append(fName+fExtension)

        # Add file names to the QListView
        model = QtGui.QStandardItemModel()
        for f in self.newFileNames:
            item = QtGui.QStandardItem(f)
            model.appendRow(item)
        self.newFileNamesList.setModel(model)

    def rename(self):
        for f in self.originalFileNames:
            fName, fExtension =  os.path.splitext(f)
            fName = re.sub(self.searchFilePatternText.text(), self.newFilePatternText.text(),fName, flags=re.I)
            os.rename(f,fName+fExtension)

        #Clear old values
        self.newFileNames.clear()
        self.originalFileNames.clear()
        self.newFilePatternText.setText("")
        self.searchFilePatternText.setText("")

        #Send confirmation message
        reply = QtGui.QMessageBox.information(self, 'Message',
                                           "Your Files Have Been Renamed.", QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Ok)

def main():
    app = QtGui.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()