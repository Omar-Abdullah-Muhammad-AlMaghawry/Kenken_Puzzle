from functools import partial
from turtle import update
from PyQt5 import QtCore, QtGui, QtWidgets

#global n

class Ui_MainWindow(object):


    def __init__(self, window):
        self.window = window
        self.n = 6

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(200, 50, 800, 500))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 111, 31))
        self.label.setObjectName("label")
        # self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(10, 190, 101, 31))
        # self.pushButton.setObjectName("pushButton")
        shift = 55
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(255 - shift, 600, 200, 30))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(555 - shift , 600, 200, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(855 - shift, 600, 200, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(40, 60, 51, 170))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 840, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Choose table size:"))
        self.pushButton_1.setText(_translate("MainWindow", "Backtracking"))
        self.pushButton_2.setText(_translate("MainWindow", "Backtracking + Forward Checking"))
        self.pushButton_3.setText(_translate("MainWindow", "Backtracking + Arc Consistency"))
        # TODO INSERT ALGORITHM FUNCTION HANDLES HERE (PROBABLY WILL NEED PARTIAL FUNCTIONS)

        self.pushButton_1.clicked.connect(self.window.algo_one)
        self.pushButton_2.clicked.connect(self.window.algo_two)
        self.pushButton_3.clicked.connect(self.window.algo_three)
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "3"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "4"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "5"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "6"))
        item = self.listWidget.item(4)
        item.setText(_translate("MainWindow", "7"))
        item = self.listWidget.item(5)
        item.setText(_translate("MainWindow", "8"))
        item = self.listWidget.item(6)
        item.setText(_translate("MainWindow", "9"))
        #"list_"
        self.listWidget.itemClicked.connect(self.list_clicked)
        self.listWidget.setSortingEnabled(__sortingEnabled)

    #Needs fixing
    def list_clicked(self, item):
        #"self."?
        self.n = int(item.text())
        # print(self.n)
        self.window.loadProducts()