from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sqlite3
from threading import Thread
from sys import argv
from DataBase.DataBaseConfiguration import Create_dataBase
import xlsxwriter
frame, _ = loadUiType("./Gui/MainWindow.ui")

class LibProject(QMainWindow, frame):
    def __init__(self, parent=None):
        super(LibProject, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Ui_Configuration()

    def Ui_Configuration(self):
        self.setWindowTitle("Library")
        #self.showMaximized()
        self.DataBase_Configuration()
        self.Sw.setCurrentIndex(0)
        self.Buttons_Configuration()
        self.Tabel_todaywork()
        self.Tabel_stok()
        self.Tabel_history()
        self.runn = True
        self.t = Thread(target=self.Get_total,args=())
        self.t.start()

    def DataBase_Configuration(self):
        try :
            self.db = sqlite3.connect("./DataBase/DataBase.db")

        except Exception:
            Create_dataBase()
            self.db = sqlite3.connect("./DataBase/DataBase.db")

        self.cur = self.db.cursor()

    def Buttons_Configuration(self):
        #TodayWork :

        self.Pb_todaywork.clicked.connect(self.Button_TodayWork)
        self.Pb_sell.clicked.connect(self.Button_sell)
        self.Pb_sell_bill.clicked.connect(self.Button_sell_bill)

        #Stok :

        self.Pb_stok.clicked.connect(self.Button_stok)
        self.Pb_save.clicked.connect(self.Button_save)

        #History :

        self.Pb_history.clicked.connect(self.Button_history)

        #Settings :

        self.Pb_settings.clicked.connect(self.Button_settings)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            self.close()
        elif e.key() == Qt.Key_Minus :
            self.Tabel_delet_row()
        elif e.key() == Qt.Key_Plus :
            self.Tabel_add_row()

    def Tabel_add_row(self):
        if self.Sw.currentIndex() == 0:
            rowcont = self.Tb_todaywork.rowCount()
            self.Tb_todaywork.insertRow(rowcont)
        elif self.Sw.currentIndex() == 1:
            rowcont = self.Tb_stok.rowCount()
            self.Tb_stok.insertRow(rowcont)

    def Tabel_delet_row(self):
        if self.Sw.currentIndex() == 0:
            rows = sorted(set(index.row() for index in
                              self.Tb_todaywork.selectedIndexes()))
            for row in rows:
                self.Tb_todaywork.removeRow(row)

        elif self.Sw.currentIndex() == 1:
            rows = sorted(set(index.row() for index in
                              self.Tb_stok.selectedIndexes()))
            for row in rows:
                self.Tb_stok.removeRow(row)

    def Fill_tabel(self,tabel,data):
        tabel.setRowCount(0)
        tabel.insertRow(0)
        for row, form in enumerate(data):
            for column, forme in enumerate(form):
                tabel.setItem(row, column, QTableWidgetItem(str(forme)))
                column += 1
            row_position = tabel.rowCount()
            tabel.insertRow(row_position)

    def Save_tabel(self,tabel):

        try:
            data = []
            self.cur.execute('''DELETE FROM Stoke''')
            for i in range(tabel.rowCount()):
                for j in range(tabel.columnCount()):
                    data.append(tabel.item(i,j).text())
                self.cur.execute('''INSERT INTO Stoke (Pr_code,Pr_Name,Pr_Quantity,Pr_Sold_Quantity,Pr_Prise ) VALUES 
                (?,?,?,?,?)''', ( int(data[0]) , data[1], int(data[2]), int(data[3]), float(data[4])))

                data.clear()
            self.db.commit()
        except Exception :
            print("data incorect ")

    def closeEvent(self,event):
        self.runn = False

    #############################   TodayWork   ######################################################################
    def Button_TodayWork(self):
        self.Sw.setCurrentIndex(0)
        self.runn = True
        self.t = Thread(target=self.Get_total,args=())
        self.t.start()

    def Button_sell(self):
        self.Sell()
        self.Tb_todaywork.setRowCount(0)
        self.Tb_todaywork.insertRow(0)
        self.TotalShow.display(0)

    def Button_sell_bill(self):
        self.Sell_Bill()
        self.Tb_todaywork.setRowCount(0)
        self.Tb_todaywork.insertRow(0)
        self.TotalShow.display(0)
    def Get_total(self):

        while self.runn :
            if self.Sw.currentIndex() == 0:
                try :
                    Total = 0
                    for i in range(self.Tb_todaywork.rowCount()) :
                        prise = int(self.Tb_todaywork.item(i,3).text())
                        quntite = int(self.Tb_todaywork.item(i,2).text())
                        prise = prise * quntite
                        Total = Total + prise
                    self.TotalShow.display(Total)
                except Exception :
                    pass
            else :
                self.runn = False

    def Tabel_todaywork(self):
        self.Tb_todaywork.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.Tb_todaywork.setRowCount(0)
        self.Tb_todaywork.insertRow(0)

    def Sell(self):
        try :
            for i in range(self.Tb_todaywork.rowCount()) :
                code = int(self.Tb_todaywork.item(i,0).text())
                sold_Quantity = int(self.Tb_todaywork.item(i,2).text())
                Quantity = int(self.Tb_todaywork.item(i,2).text())
                self.cur.execute('''SELECT Pr_Sold_Quantity FROM Stoke WHERE Pr_code = ?''',(code,))
                data = self.cur.fetchone()
                Quantity = data[0] - Quantity
                self.cur.execute('''UPDATE Stoke SET Pr_Quantity = ? , Pr_Sold_Quantity = ? WHERE Pr_code = ? ''',(Quantity,sold_Quantity,code))
                self.db.commit()
        except Exception :
            pass

    def Sell_Bill(self):
        try :
            for i in range(self.Tb_todaywork.rowCount()) :
                code = int(self.Tb_todaywork.item(i,0).text())
                sold_Quantity = int(self.Tb_todaywork.item(i,2).text())
                Quantity = int(self.Tb_todaywork.item(i,2).text())
                self.cur.execute('''SELECT Pr_Sold_Quantity FROM Stoke WHERE Pr_code = ?''',(code,))
                data = self.cur.fetchone()
                Quantity = data[0] - Quantity
                self.cur.execute('''UPDATE Stoke SET Pr_Quantity = ? , Pr_Sold_Quantity = ? WHERE Pr_code = ? ''',(Quantity,sold_Quantity,code))
                self.db.commit()
        except Exception :
            pass

    ###################################   stok   #####################################################################
    def Button_stok(self):
        self.Sw.setCurrentIndex(1)
        self.Tabel_stok()
    def Button_save(self):
        self.Save_tabel(self.Tb_stok)

    def Tabel_stok(self):
        self.Tb_stok.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.cur.execute('''SELECT Pr_code,Pr_Name,Pr_Quantity,Pr_Sold_Quantity,Pr_Prise FROM Stoke''')
        data = self.cur.fetchall()
        self.Fill_tabel(self.Tb_stok,data)

    ####################################   History   #################################################################
    def Button_history(self):
        self.Sw.setCurrentIndex(2)

    def Tabel_history(self):
        self.Tb_history.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    ###################################    Settings    ###############################################################
    def Button_settings(self):
        self.Sw.setCurrentIndex(3)

    def test(self):
        print("test Pb_settings")
    def enebel(self):
        pass

def Draw_ui():
    app = QApplication(argv)
    window = LibProject()
    window.show()
    app.exec_()

if __name__ == '__main__':
    Draw_ui()
