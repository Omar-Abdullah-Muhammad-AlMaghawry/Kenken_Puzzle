from random import sample
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import PyQt5
from PyQt5.QtWidgets import QTableWidgetItem
import numpy
from tablewidget import Ui_MainWindow
from randomize_grid import randomize_cages, randomize_grid


class Window(QtWidgets.QMainWindow) :
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Kenken")
        #self.setGeometry(500, 500, 1000, 600)
        #self.setWindowIcon(QtGui.QIcon(''))
        self.ui = Ui_MainWindow(self)
        self.ui.setupUi(self)
        self.loadProducts()
        self.cages
        self.solved = False
        self.rarr

    def loadProducts(self):
        self.solved = False

        #insert n here from list (replace the 3)
        self.ui.tableWidget.setRowCount(self.ui.n)
        self.ui.tableWidget.setColumnCount(self.ui.n)

        #(index, width) probably for loop for j in n: setColumnWidth(i, 100)
        for i in range(self.ui.n+1):
            self.ui.tableWidget.setColumnWidth(i, 85)

        # (index, width) probably for loop for i in n: setRowHeight(i, 100)
        for i in range(self.ui.n+1):
            self.ui.tableWidget.setRowHeight(i, 50)

        for i in range(self.ui.n):
            for j in range(self.ui.n):       
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(""))
                self.ui.tableWidget.item(i, j).setTextAlignment(PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignLeft)
        
        self.rarr = randomize_grid(self.ui.n)
        self.cages = randomize_cages(self.rarr)
        # (row(for loop i), column(for loop j), QTableWidetItem('%d', rarr[idx]))
        for cage in self.cages:
            cells = cage[0]
            color = sample(range(100, 255), 3)
            rule_row, rule_col = 10, 10
            for cell in cells:
                self.ui.tableWidget.item(cell[0], cell[1]).setBackground(QtGui.QColor(color[0],color[1],color[2]))
                if(cell[0] < rule_row):
                    rule_row = cell[0]
                    rule_col = cell[1]
                elif(cell [0] == rule_row):
                    if(cell[1] < rule_col):
                        rule_row = cell[0]
                        rule_col = cell[1]
            self.ui.tableWidget.item(rule_row, rule_col).setText(cage[1] + " {" + str(cage[2]) + "}" )
        
    def fillTable(self, solution):
        self.solved = True
        for i in range(self.ui.n):
            for j in range(self.ui.n):
                existing = self.ui.tableWidget.item(i, j).text()
                self.ui.tableWidget.item(i, j).setText(existing + "\n" + str(solution[i][j]))

    def algo_one(self):
        if(not self.solved):
            self.fillTable(self.rarr)
    
    def algo_two(self):
        if(not self.solved):
            self.fillTable(self.rarr)

    def algo_three(self):
        if(not self.solved):
            self.fillTable(self.rarr)


def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

create_app()



#if __name__ == '__main__':



