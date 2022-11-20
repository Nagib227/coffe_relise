import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from change_Dialog import Change_Dialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_UI.ui', self)
        self.con = sqlite3.connect("coffee_db.sqlite")
        self.pushButton.clicked.connect(self.open_change)
        self.pushButton_2.clicked.connect(self.open_add)
        self.loadTable()

    def loadTable(self):
        res = self.con.cursor().execute("""SELECT * FROM coffee""").fetchall()
        title = ["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена",
                 "объем упаковки"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
                self.x = i
                self.y = j
        self.tableWidget.resizeColumnsToContents()

    def open_add(self):
        self.Use_Dialog = Change_Dialog(self)
        self.Use_Dialog.show()

    def open_change(self):
        xs = []
        cells = 0
        prov = False
        for i in range(self.x + 1):
            for j in range(self.y + 1):
                if self.tableWidget.item(i, j).isSelected() and i not in xs:
                    cells += 1
                    xs.append(i)
                    prov = True
        if not prov:
            self.statusBar().showMessage('Выберете ячейку')
            return None
        elif cells > 1:
            self.statusBar().showMessage('Выберете одну ячейку')
            return None
        for it in self.tableWidget.selectedItems():
            x = it.row()
        change = []
        for i in range(self.y + 1):
            change.append(self.tableWidget.item(x, i).text())
        self.id = change[0]
        self.Use_Dialog = Change_Dialog(self, change)
        self.Use_Dialog.show()

    def close_change(self):
        use = self.Use_Dialog.returnVal()
        if not use[0] or not use[1] or not use[2] or not use[3] \
                or not use[4] or not use[5]:
            self.statusBar().showMessage('Некорректные данные')
            self.Use_Dialog.destroy()
            return None
        self.con.cursor().execute(f"""UPDATE coffee
        SET title = '{use[0]}',
        degFRoast = '{use[1]}', 
        gro_gra = '{use[2]}',
        taste = '{use[3]}',
        price = '{use[4]}',
        pacVol = '{use[5]}'
        WHERE id = {self.id}""")
        self.Use_Dialog.destroy()
        self.con.commit()
        self.loadTable()

    def close_add(self):
        use = self.Use_Dialog.returnVal()
        if not use[0] or not use[1] or not use[2] or not use[3] \
                or not use[4] \
                or not use[5]:
            self.statusBar().showMessage('Некорректные данные')
            self.Use_Dialog.destroy()
            return None
        self.con.cursor().execute(f"""INSERT INTO coffee(title, degFRoast, gro_gra,
            taste, price, pacVol)
VALUES('{use[0]}', '{use[1]}', '{use[2]}', '{use[3]}', '{use[4]}', '{use[5]}')""")
        self.Use_Dialog.destroy()
        self.con.commit()
        self.loadTable()

    def closeEvent(self, event):
        self.con.commit()
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())