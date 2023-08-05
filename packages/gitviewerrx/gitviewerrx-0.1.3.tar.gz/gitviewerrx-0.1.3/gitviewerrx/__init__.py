# -*- coding: utf-8 -*-

import sys
import os
import subprocess

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout, QLabel,  QGridLayout
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItemModel
from PyQt5.QtCore import QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,QTime,QPersistentModelIndex


class App(QWidget):
    
    SHA, FROM, SUBJECT, DATE = range(4)
    
    def __init__(self):
        super(App,self).__init__()
        self.title = 'Git Commit History Browser'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        model = self.createCommitModel(self)
        self.modelGit = model
        #########################
        ## button: get commit log
        self.btn = QPushButton('Filter', self)
        self.btn.clicked.connect(self.getGitHistory)
        self.btn.setFixedWidth(110)
        
        #########################
        ## label: input search
        header = QLabel('Choose Git Controlled Project Path')
        self.footer = QLabel('Notes:')

        #########################
        ## input search
        lbByDate = QLabel('Filter By Date')
        lbByRev = QLabel('Filter By Revision From')
        lbByRev2 = QLabel('To')
        self.searchEdit = QLineEdit()
        self.searchEditRevFrom = QLineEdit()
        self.searchEditRevTo = QLineEdit()
        
        self.btnGroupBox = QGroupBox()

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(lbByDate)
        btnLayout.addWidget(self.searchEdit)
        #btnLayout.addWidget(self.btn)
        
        self.btnGroupBox.setLayout(btnLayout)


        self.btnGroupBoxRow2 = QGroupBox()
        
        btnLayoutRow2 = QHBoxLayout()
        btnLayoutRow2.addWidget(lbByRev)
        btnLayoutRow2.addWidget(self.searchEditRevFrom)
        btnLayoutRow2.addWidget(lbByRev2)
        btnLayoutRow2.addWidget(self.searchEditRevTo)

        self.btnGroupBoxRow2.setLayout(btnLayoutRow2)


        self.btnGroupBoxRow3 = QGroupBox()
        btnLayoutRow3 = QHBoxLayout()
#        btnLayoutRow3.addWidget(QLineEdit())
        btnLayoutRow3.addWidget(self.btn)
        self.btnGroupBoxRow3.setLayout(btnLayoutRow3)

        #########################
        ## Tree view of folder
        self.model = QFileSystemModel()
        self.model.setRootPath('')
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        
        self.tree.setAnimated(False)
        self.tree.setIndentation(20) # set indentation for each block in tree view
        self.tree.setSortingEnabled(True)
        

        #########################
        ## tree view of git comment history
        self.dataGroupBox = QGroupBox("Histroy")
        self.dataView = QTreeView()
        self.dataView.setModel(model)
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)


        #########################
        # set windwoLayout
        #########################
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(header)
        windowLayout.addWidget(self.tree)
        windowLayout.addWidget(self.btnGroupBox)
        windowLayout.addWidget(self.btnGroupBoxRow2)
        windowLayout.addWidget(self.btnGroupBoxRow3)
#        windowLayout.addWidget( self.btn )
        windowLayout.addWidget(self.dataGroupBox)
        windowLayout.addWidget(self.footer)
        
        self.setLayout(windowLayout)
        self.show()
        
    def createCommitModel(self,parent):
        model = QStandardItemModel(0, 4, parent)
        model.setHeaderData(self.SHA, Qt.Horizontal, "SHA-1")
        model.setHeaderData(self.DATE, Qt.Horizontal, "Date")
        model.setHeaderData(self.FROM, Qt.Horizontal, "Author")
        model.setHeaderData(self.SUBJECT, Qt.Horizontal, "Commit")

        return model

    def addCommitInfo(self, model, who, subject, date, detail):
        model.insertRow(0)
        model.setData(model.index(0, self.DATE), date)
        model.setData(model.index(0, self.FROM), who)
        model.setData(model.index(0, self.SUBJECT), subject)
        model.setData(model.index(0, self.SHA), detail)

    def removeCommitInfo(self, model):
        n = model.rowCount()
        for i in range(n):
            model.removeRow(0)

    def clearAllCommitInfo(self, model):
        model.clear()

    def getGitHistory(self):
        print "clean tree"
        self.removeCommitInfo(self.modelGit)

        index = self.tree.currentIndex()
        print self.model.filePath(index)
        self.projectPath = self.model.filePath(index)
        self.footer.setText("Notes: "+"path:"+self.projectPath)
        words = self.searchEdit.text()
        wordsRevFrom = self.searchEditRevFrom.text()
        wordsRevTo = self.searchEditRevTo.text()

        self.noteMsg = "Notes: "
        cmd = self.phaseCmd(words, self.projectPath, wordsRevFrom, wordsRevTo)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = p.communicate()
    
#        # Debug
#        print "---"
#        print out
#        print "---"
#        print err[:-1]
#        print "---"

        lines = out.split("\n")
        linesErr = err[:-1].split("\n")

        for l in linesErr:
            if "fatal: Not a git repository" in l or "fatal: bad default revision 'HEAD'" in l:
                self.noteMsg = self.noteMsg +"fatal: Not a git repository. "+"PLEASE CHOOSE RIGHT FOLDER. "
                print "here "
            elif "fatal: ambiguous argument" in l and "unknown revision" in l:
                self.noteMsg = self.noteMsg + "fatal: ambiguous argument, " + "unknown revision "
                print "there "
            elif len(l)==0:
                continue
            else:
                print "Unknown fatal msg: " + l
        self.footer.setText(self.noteMsg)

        for l in lines[::-1]:
            if len(l)==0:
                continue
            else:
                arr = l[1:-1].split("\t")
                sha = arr[0]
                auther = arr[1]
                date = arr[2]
                commit = arr[3]
                self.addCommitInfo(self.modelGit, auther, commit, date, sha)


    def phaseCmd(self,words, path,  wordsRevFrom, wordsRevTo):
#        cmd = ["git", "-C", path, "log"]
        cmd = ["git", "--git-dir", path+"/.git", "log"]
        
        if words != "":
            if "ago" in words or "since" in words or "after" in words:
                cmd.append("--since=\""+words+"\"")
            elif "until" in words or "before" in words:
                cmd.append("--until=\""+words+"\"")
            else:
                self.noteMsg = self.noteMsg + "Unrecognized filter for git. Update table without ByDate filter. "
                print "unrecognized filter"
    
        # www.kernel.org/pub/software/scm/git/docs/git-rev-parse.html
        if wordsRevFrom == "" and wordsRevTo == "":
            cmd = cmd
        elif wordsRevFrom == "":
            cmd.append(wordsRevTo)
        else:
            cmd.append(wordsRevFrom + "..." + wordsRevTo)

        cmd.append("--date=local")
        cmd.append("--pretty=format:\"%h%x09%an%x09%ad%x09%s\"")
        return cmd



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    
    sys.exit(app.exec_())


