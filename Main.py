import sys
import re
import os
from PyQt4 import QtGui, QtCore


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):

        #Variables for determining source folder
        self.folderBtn = QtGui.QPushButton("Select Folder", self)
        self.folderBtn.clicked.connect(self.selectFolder)
        self.folderPath = QtGui.QLineEdit()

        #Variables for detrmining how the files are renamed
        self.originalFilePattern = QtGui.QLineEdit()
        self.newFilePattern = QtGui.QLineEdit()

        self.runBtn = QtGui.QPushButton("Rename", self)
        self.runBtn.clicked.connect(self.rename)
        self.pythonRegexCheck = QtGui.QLabel('Use Python Regex', self)

        #Determine if looking for a certain file extention or not
        self.fileExtension = QtGui.QLineEdit(".txt", self)
        self.fileExtentionCheck = QtGui.QCheckBox('Modify All File Extentions', self)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.folderBtn, 1, 0)
        grid.addWidget(self.folderPath, 1, 1)
        grid.addWidget(self.originalFilePattern, 2, 0,QtCore.Qt.AlignLeft)
        grid.addWidget(self.newFilePattern, 2, 1, QtCore.Qt.AlignRight)
        grid.addWidget(self.pythonRegexCheck,3 ,0)
        grid.addWidget(self.fileExtension, 4,0)
        grid.addWidget(self.fileExtentionCheck,4,1)
        grid.addWidget(self.runBtn, 5,1, QtCore.Qt.AlignCenter)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File Renamer')
        self.show()

    #Dialog for getting folder path
    def selectFolder(self):
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.folderPath.setText(file)

    #These two functions parse the pattern into regex
    def parseOriginalFilePattern(self):
        print("Hello")

    def parseNewFilePattern(self):
        print("Hello")

    def rename(self):
        os.chdir(self.folderPath.text())
        if not self.fileExtentionCheck.isChecked() :
            listFiles = [f for f in os.listdir(self.folderPath.text()) if os.path.splitext(f)[1] == self.fileExtension.text()]
        else :
            listFiles = [f for f in os.listdir(self.folderPath.text())]

        for f in listFiles:
            fName, fExtension =  os.path.splitext(f)

            fName = re.sub(self.originalFilePattern.text(), self.newFilePattern.text(),fName, flags=re.I)
            #print(fName)
            os.rename(f,fName+fExtension)

def main():
    app = QtGui.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()