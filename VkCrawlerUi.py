# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vk-crawler.ui'
#
# Created: Sat May 18 12:37:26 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(651, 543)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 651, 491))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.saveToFolderLineEdit = QtGui.QLineEdit(self.tab)
        self.saveToFolderLineEdit.setObjectName(_fromUtf8("saveToFolderLineEdit"))
        self.gridLayout.addWidget(self.saveToFolderLineEdit, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.chooseSaveFolderButton = QtGui.QPushButton(self.tab)
        self.chooseSaveFolderButton.setObjectName(_fromUtf8("chooseSaveFolderButton"))
        self.gridLayout.addWidget(self.chooseSaveFolderButton, 1, 2, 1, 1)
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.linkToTargetLineEdit = QtGui.QLineEdit(self.tab)
        self.linkToTargetLineEdit.setInputMask(_fromUtf8(""))
        self.linkToTargetLineEdit.setObjectName(_fromUtf8("linkToTargetLineEdit"))
        self.gridLayout.addWidget(self.linkToTargetLineEdit, 0, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.columnView = QtGui.QColumnView(self.tab)
        self.columnView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.columnView.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.columnView.setObjectName(_fromUtf8("columnView"))
        self.verticalLayout.addWidget(self.columnView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cancelButton = QtGui.QPushButton(self.tab)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.downloadButton = QtGui.QPushButton(self.tab)
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))
        self.horizontalLayout.addWidget(self.downloadButton)
        self.scanButton = QtGui.QPushButton(self.tab)
        self.scanButton.setObjectName(_fromUtf8("scanButton"))
        self.horizontalLayout.addWidget(self.scanButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressBar = QtGui.QProgressBar(self.tab)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 651, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionCredentials = QtGui.QAction(MainWindow)
        self.actionCredentials.setObjectName(_fromUtf8("actionCredentials"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuOptions.addAction(self.actionCredentials)
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.saveToFolderLineEdit.setPlaceholderText(_translate("MainWindow", "your downloaded files will be saved here", None))
        self.label_2.setText(_translate("MainWindow", "Save to folder:", None))
        self.chooseSaveFolderButton.setText(_translate("MainWindow", "Choose", None))
        self.label.setText(_translate("MainWindow", "Link to target:", None))
        self.linkToTargetLineEdit.setPlaceholderText(_translate("MainWindow", "http://vk.com/id1234", None))
        self.cancelButton.setText(_translate("MainWindow", "Cancel", None))
        self.downloadButton.setText(_translate("MainWindow", "Download", None))
        self.scanButton.setText(_translate("MainWindow", "Scan", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))
        self.menuOptions.setTitle(_translate("MainWindow", "options", None))
        self.menuHelp.setTitle(_translate("MainWindow", "help", None))
        self.menuFile.setTitle(_translate("MainWindow", "file", None))
        self.actionCredentials.setText(_translate("MainWindow", "credentials", None))
        self.actionAbout.setText(_translate("MainWindow", "about", None))
        self.actionExit.setText(_translate("MainWindow", "exit", None))

