import PySimpleGUI as sg
import psycopg2
import DBprovider

from DBprovider import *

class UI_MainWindow():

    def __init__(self,UserLogin,UserPassword):
        tab1_layout =  [[sg.Text('IP адрес подключения:',size=(20,1)),sg.Input(size=(20,1),default_text=('192.168.2.100'),key=('-HOST-'))],
                [sg.Text('Порт:',size=(20,1)),sg.Input(size=(20,1),default_text =('5432'),key=('-PORT-'))],
                [sg.Text('Имя базы данных:',size=(20,1)),sg.Input(size=(20,1),default_text=('postgres'),key=('-DATABASE-'))],
                [sg.Button('Проверить подключение')]]
        '''
        data = []
        headings = []
        SQLtables = []
        i = 0
        

        tab2_layout = [[sg.Combo(values=SQLtables, key=('-COMBOTABLES-'),size=(20,1), auto_size_text=True),
                        sg.Button(button_text=('Получить список таблиц'),size=(20,1)),
                        sg.Button(button_text=('Получить записи из таблицы'),key=('-GETTABLES-'),size=(20,1),disabled=True)],
                       [sg.Frame('',[[sg.T('')]], key='-COL1-')]]
        '''
        users = []

        tab2_layout = [[sg.Input(size=(80,1),key=('-EXPRESSION-'))],
                       [sg.Multiline(auto_size_text=True, key=('-EXPRRESULT-'), size=(80,20))],
                       [sg.Button(button_text=('Выполнить запрос'),key=('-RUNEXPRESSION-'),size=(20,1))]]

        tab3_layout = [[sg.Button(button_text=('Получить данные о пользователях'), key=('-GETUSERSDATA-'), size=(30, 1))],
                       [sg.Multiline(auto_size_text=True, key=('-USERSDATA-'), size=(100, 10))],
                       [sg.Frame('',[[sg.Text('Изменить параметры пользователя')],
                                 [sg.Combo(values = users, size = (20,1), auto_size_text=True,key='-USERSCOMBO-')],
        [sg.T('Username'),sg.T('usesysid'),sg.T('usecreatedb'),sg.T('usesuper'),sg.T('userepl'),sg.T('usebypassrls'),sg.T('valuntil'),sg.T('useconfig')]])]]
        #CREATEDB, CREATEROLE, CREATEUSER, and even SUPERUSER
        #NOCREATEDB, NOCREATEROLE, NOCREATEUSER ,NOSUPERUSER

        column_to_be_centered = [[sg.TabGroup(
            [[sg.Tab('Подключение к БД', tab1_layout),
             sg.Tab('Работа с БД', tab2_layout,disabled=True, key= ('-TAB2-')),
              sg.Tab('Работа с пользователями БД',tab3_layout, disabled=True, key = ('-TAB3-'))]],
            key=('-TABS-'))]]

        layout = [[sg.Text(key='-TOPEXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
                  [sg.Text('', pad=(0, 0), key='-LEFTEXPAND-'),  # the thing that expands from left
                   sg.Column(column_to_be_centered, vertical_alignment='center', justification='center', k='-C-'),
                   sg.Text('', pad=(0, 0), key='-RIGHTEXPAND-')]]

        window = sg.Window('Window Title', layout, resizable=True, finalize=True)
        window['-C-'].expand(True, True, True)
        window['-TOPEXPAND-'].expand(True, True, True)
        window['-LEFTEXPAND-'].expand(True, False, True)
        window['-RIGHTEXPAND-'].expand(True, False, True)
        window['-TABS-'].expand(True, True, True)

#        window = sg.Window('MainWindow', layout)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                cur.close()
                connection.close()
                window.close()
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

                    if (connection.closed == 0):
                       sg.Popup('Title', 'Соединение установлено')
                       window['-TAB2-'].update(disabled=False)
                       window['-TAB3-'].update(disabled=False)

                except Exception as error:
                    sg.Popup('Title', 'Соединение не установлено', error.args)
            elif event == 'Получить список таблиц':
                window['-GETTABLES-'].update(disabled=False)
                cur.execute("select table_name from information_schema.tables where table_schema = 'public';")
                SQLtables = cur.fetchall()
                window['-COMBOTABLES-'].update(values=SQLtables)

            elif event == '-RUNEXPRESSION-':
                try:
                    print(values['-EXPRESSION-'])
                    cur.execute(values['-EXPRESSION-'])
                    window['-EXPRRESULT-'].update(cur.fetchall(),append=True)

                except Exception as error:
                    sg.Popup('Ошибка', error.args)

            elif event == '-GETUSERSDATA-':
                try:

                    db = DBprovider.DBProvider("")
                    db.get_users(cur)
                    headings = db.headings
                    data = db.userdata
                    print(headings)
                    print(data)

                    window['-USERSDATA-'].update(str(headings).replace(",", " |"), append=True)
                    window['-USERSDATA-'].update(("\n"), append=True)
                    window['-USERSDATA-'].update(str(data).replace(","," |"), append=True)
                    window['-USERSCOMBO-'].update(values=db.userNames)

                except Exception as error:
                    sg.Popup('Ошибка', error.args)
            elif event == '-USERSCOMBO-':
                sg.Popup('ComboDetected')
            #elif event == '-GETTABLES-':
            #    try:
                    #tablename = str(values['-COMBOTABLES-']).replace("(" ,"").replace(")" ,"").replace("'" ,"").replace(",","")
                    #cur.execute("SELECT * FROM {0}".format(tablename))
                    #cur.execute("select column_name from information_schema.columns where information_schema.columns.table_name='{0}';".format(tablename))

             #   except Exception as error:
             #       sg.Popup('Ошибка', error.args)

