from dialog_UI import Ui_Dialog
from PyQt5.QtWidgets import QDialog


class Change_Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None, change=[]):
        super(Change_Dialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        if not len(change):
            self.pushButton.setText("Добавить")
            self.pushButton.clicked.connect(self.parent.close_add)
        else:
            self.lineEdit.setText(change[1])
            self.lineEdit_2.setText(change[2])
            self.lineEdit_3.setText(change[3])
            self.lineEdit_4.setText(change[4])
            self.lineEdit_5.setText(change[5])
            self.lineEdit_6.setText(change[6])
            self.pushButton.setText("Сохранить")
            self.pushButton.clicked.connect(self.parent.close_change)  #######

    def returnVal(self):
        return [self.lineEdit.text(), self.lineEdit_2.text(),
                self.lineEdit_3.text(), self.lineEdit_4.text(),
                self.lineEdit_5.text(), self.lineEdit_6.text()]

    def closeEvent(self, event):
        self.parent.show()
