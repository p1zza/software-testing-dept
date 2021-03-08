import sys

from PyQt5 import QtGui, QtWidgets

from LoginWindow import Ui_Login

import psycopg2

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.form_widget = Ui_Login(self)
        _widget = QtWidgets.QWidget()
        #_layout = QtWidgets.QGridLayout(_widget)
        #_layout.setGeometry(MainWindow.geometry(self))
        #_layout = QtWidgets.QVBoxLayout(_widget)
        #_layout.addWidget(self.form_widget)
        self.setCentralWidget(self.form_widget)

        self.form_widget.loginButton.clicked.connect(self.InitLogin)

    def InitLogin(self):
        try:
            connection = psycopg2.connect(
                host="192.168.2.100",
                port=5432,
                database="postgres",
                user= self.form_widget.Login_textBox.toPlainText(),
                password=self.form_widget.Password_textBox.toPlainText(),
                connect_timeout=3,
                keepalives_idle=5,
                keepalives_interval=2,
                keepalives_count=2)

            cur = connection.cursor()
            cur.execute("SELECT datname,usename,client_addr,client_port FROM pg_stat_activity;")
            query_results = cur.fetchall()
            print(query_results)

            if (connection.closed==0) :
                msg = QtWidgets.QMessageBox(parent=self)
                msg.setText("Подключение есть")
                self.setCentralWidget(msg)



        except Exception as error:
            msg = QtWidgets.QMessageBox(parent=self)
            msg.setText(str(error))
            msg.setWindowTitle("MessageBox demo")
            msg.setDetailedText(str(error.args))
            msg.exec_()

        finally:
            cur.close()
            connection.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 
