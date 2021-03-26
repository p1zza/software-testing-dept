import psycopg2

from UI_MainWindow import UI_MainWindow
from UI_LoginWindow import UI_LoginWindow



lg = UI_LoginWindow()
UserLogin = lg.UserLogin
UserPassword = lg.UserPassword

mw = UI_MainWindow(UserLogin,UserPassword)
'''


connection = psycopg2.connect(
    host="192.168.2.102",
    port=5432,
    database="postgres",
    user=UserLogin,
    password=UserPassword,
    connect_timeout=3,
    keepalives_idle=5,
    keepalives_interval=2,
    keepalives_count=2)

if (connection.closed == 0):
    msg.setText("Подключение есть")
    self.setCentralWidget(msg)

cur = connection.cursor()
cur.execute("SELECT datname,usename,client_addr,client_port FROM pg_stat_activity;")
query_results = cur.fetchall()
print(query_results)
'''
