import PySimpleGUI as sg

import psycopg2

class UI_MainWindow():
    def __init__(self,UserLogin,UserPassword):
        tab1_layout =  [[sg.Text('IP адрес подключения:',size=(20,1)),sg.Input(size=(20,1),default_text=('192.168.2.102'),key=('-HOST-'))],
                [sg.Text('Порт:',size=(20,1)),sg.Input(size=(20,1),default_text =('5432'),key=('-PORT-'))],
                [sg.Text('Имя базы данных:',size=(20,1)),sg.Input(size=(20,1),default_text=('postgres'),key=('-DATABASE-'))]]

        tab2_layout = [[sg.T('This is inside tab 2')],
                       [sg.In(key='in')]]
        layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 2', tab2_layout)]])],
              [sg.Button('Проверить подключение')]]

        window = sg.Window('MainWindow',layout)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == 'Проверить подключение':

                try:
                    connection = psycopg2.connect(
                        host=values['-HOST-'],
                        port=values['-PORT-'],
                        database=values['-DATABASE-'],
                        user=UserLogin,
                        password=UserPassword,
                        connect_timeout=3,
                        keepalives_idle=5,
                        keepalives_interval=2,
                        keepalives_count=2)
                    cur = connection.cursor()
                    cur.execute("SELECT datname,usename,client_addr,client_port FROM pg_stat_activity;")
                    query_results = cur.fetchall()
                    print(query_results)
                    cur.close()
                    connection.close()

                    if (connection.closed == 0):
                       sg.Popup('Title','Соединение установлено')

                except Exception as error:
                    sg.Popup('Title', 'Соединение не установлено',error,error.args)

                #print(str(values['-PORT-']),str(values['-HOST-']),str(values['-DATABASE-']))
            window.close()


