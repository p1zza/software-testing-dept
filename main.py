import psycopg2

from UI_MainWindow import UI_MainWindow
from UI_LoginWindow import UI_LoginWindow



lg = UI_LoginWindow()
UserLogin = lg.UserLogin
UserPassword = lg.UserPassword

mw = UI_MainWindow(UserLogin, UserPassword)