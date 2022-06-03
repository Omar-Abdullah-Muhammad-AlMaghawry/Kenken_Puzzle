from random import sample
import string
import sys
from unittest import result
from PyQt5 import QtGui, QtCore, QtWidgets
import PyQt5
from PyQt5.QtWidgets import QTableWidgetItem
import numpy
from tablewidget import Ui_MainWindow
from randomize_grid import randomize_cages, randomize_grid
import csp
import kenken

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
        self.lines = []

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
                index = 'K' + str(i) + str(j)
                val = solution[index]
                # sys.stdout.write(str(sol[string]) + " ")
                existing = self.ui.tableWidget.item(i, j).text()
                self.ui.tableWidget.item(i, j).setText(existing + "\n" + str(val))

    def getLines(self):
        for cage in self.cages:
                var = cage[0]
                op= cage[1]
                val = cage[2]
                strVar = str(var)
                l = strVar.split()
                varSt = ""
                for l1 in l:
                    varSt += l1 
                # varSt.join(l)
                # print(varSt)
                self.lines.append( varSt + " "+ str(op) + " " + str(val) + "\n" )
                # print(lines)  
    def algo_one(self):
        if(not self.solved):
            size = self.ui.n
            self.getLines()
            # lines = lines[0:-1]
            # print(lines)
            kenken1 = kenken.KenKen(size, self.lines)

            game_kenken1 = csp.Constrain_Satsified_Problem(kenken1.vars, kenken1.domains, kenken1.adjecent, kenken1.constraint)
            kenken1.insertGame(game_kenken1)

            resultDec = csp.backtracking_search(game_kenken1)
           
            self.fillTable(resultDec)
    
    def algo_two(self):
       if(not self.solved):
            size = self.ui.n
            self.getLines()
            # lines = lines[0:-1]
            # print(lines)
            kenken1 = kenken.KenKen(size, self.lines)

            game_kenken1 = csp.Constrain_Satsified_Problem(kenken1.vars, kenken1.domains, kenken1.adjecent, kenken1.constraint)
            kenken1.insertGame(game_kenken1)

            resultDec = csp.backtracking_search(game_kenken1,inference=csp.forwardCheckingFn)
           
            self.fillTable(resultDec)
    def algo_three(self):
       if(not self.solved):
            size = self.ui.n
            self.getLines()
            # lines = lines[0:-1]
            # print(lines)
            kenken1 = kenken.KenKen(size, self.lines)

            game_kenken1 = csp.Constrain_Satsified_Problem(kenken1.vars, kenken1.domains, kenken1.adjecent, kenken1.constraint)
            kenken1.insertGame(game_kenken1)

            resultDec = csp.backtracking_search(game_kenken1, inference=csp.mac)
           
            self.fillTable(resultDec)

def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

create_app()



#if __name__ == '__main__':



