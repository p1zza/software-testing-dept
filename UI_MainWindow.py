import PySimpleGUI as sg
import psycopg2
import DBprovider
import paramiko

from DBprovider import *
ip = '192.168.2.101'

class UI_MainWindow():

    def __init__(self,UserLogin,UserPassword):
        tab1_layout =  [[sg.Text('IP адрес подключения:',size=(20,1)),sg.Input(size=(20,1),default_text=ip,key=('-HOST-'))],
                [sg.Text('Порт:',size=(20,1)),sg.Input(size=(20,1),default_text =('5432'),key=('-PORT-'))],
                [sg.Text('Имя базы данных:',size=(20,1)),sg.Input(size=(20,1),default_text=('postgres'),key=('-DATABASE-'))],
                [sg.Button('Проверить подключение')]]

        users = []
        tables = []

        tab2_layout = [[sg.Input(size=(80,1),key=('-EXPRESSION-'))],
                       [sg.Multiline(auto_size_text=True, key=('-EXPRRESULT-'), size=(80,20))],
                       [sg.Button(button_text=('Выполнить запрос'),key=('-RUNEXPRESSION-'),size=(20,1))]]

        tab3_layout = [
                        [sg.Button(button_text=('Получить данные о пользователях'), key=('-GETUSERSDATA-'), size=(30, 1))],
                        [sg.Multiline(auto_size_text=True, key=('-USERSDATA-'), size=(100, 10))],
                        [sg.Frame('',[[sg.Text('Изменить параметры пользователя')],
                        [   sg.Listbox(values = users, size = (20,2), auto_size_text=True,key='-USERSCOMBO-'),
                            sg.Listbox(values = tables, size = (20,2), auto_size_text=True,key='-TABLESCOMBO-'),
                            sg.Listbox(values = tables, size = (20,2), auto_size_text=True,key='-TABLESPRIVCOMBO-'),
                            sg.Listbox(values = ["GRANT","REVOKE"], size = (20,2), auto_size_text=True,key='-TABLESSETTINGSCOMBO-')],
                         [sg.Button(button_text=('Выполнить'), key=('-EXECPRIV-'), size=(30, 1))]])],
                       [sg.Frame('',[[sg.Text('Настроить права пользователя к таблицам'),
                                      sg.Combo(values = users, size = (20,1), auto_size_text=True,key='-USERSCOMBO1-'),
                                      sg.Button(button_text="Получить данные",key=('-GETUSERPRIV-'))],
                            [sg.Multiline(auto_size_text=True, key=('-TABLEPRIVELEGIES-'), size=(60, 10))]]),
                            sg.Frame('', [sg.Text('Добавить нового пользователя'),
                                           [sg.Text('Имя пользователя:'),sg.Input(key='-NEWUSERNAME-'),
                                                sg.Button(button_text="Создать пользователя", key=('-USERCREATE-'),size=(30, 1))],
                                           [sg.Checkbox('Superuser',enable_events=True, key='-SUPERUSER-CHECKBOX-')],
                                           [sg.Checkbox('CreateDB',enable_events=True, key='-CreateDB-CHECKBOX-')],
                                           [sg.Checkbox('CreateRole', enable_events=True, key='-CreateRole-CHECKBOX-')],
                                           [sg.Checkbox('INHERIT', enable_events=True, key='-INHERIT-CHECKBOX-')],
                                           [sg.Checkbox('LOGIN', enable_events=True, key='-LOGIN-CHECKBOX-')]
                                           ])
                        ]
                      ]


        tab4_layout = [[sg.Button(button_text=('Получить данные о проектах'), key=('-GETPROJECTSDATA-'), size=(20, 1))],
             [sg.Multiline(auto_size_text=True, key=('-PROJDATARESULTS-'), size=(80, 10)),
                        sg.Listbox(key=("-PROJLIST-"),size=(40,10),
                                   values=["Список проектов"],auto_size_text=True)],
                       [sg.Button(button_text=('Скопировать проект на локальную машину'), key=('-COPYPROJ-')),
                        sg.Text("Нажмите на проект, и тыкните на кнопку, чтобы скопировать его на локальную машину",auto_size_text=True)],
                       [sg.Multiline(auto_size_text=True, key=('-SSHRESULT-'), size=(80, 10))]]

        column_to_be_centered = [[sg.TabGroup(
            [[sg.Tab('Подключение к БД', tab1_layout),
             sg.Tab('Работа с БД', tab2_layout,disabled=True, key= ('-TAB2-')),
              sg.Tab('Работа с пользователями БД',tab3_layout, disabled=True, key = ('-TAB3-')),
               sg.Tab('Проекты', tab4_layout, disabled=True, key=('-TAB4-'))]],
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
                       window['-TAB4-'].update(disabled=False)

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
                    window['-USERSCOMBO1-'].update(values=db.userNames)

                except Exception as error:
                    sg.Popup('Ошибка', error.args)

            elif event == '-GETUSERPRIV-':
                try:
                    user = values["-USERSCOMBO1-"]
                    db = DBprovider.DBProvider("")
                    db.get_privelegies(cur,user)
                    window['-TABLEPRIVELEGIES-'].update(" ",append = False)
                    window['-TABLEPRIVELEGIES-'].update(str(db.privelegies).replace("),","\n"))
                    window['-TABLESCOMBO-'].update(values=db.uniquetables)
                    window['-TABLESPRIVCOMBO-'].update(values=db.uniqueprivtypes)

                except Exception as error:
                    sg.Popup('Ошибка', error.args)
            elif event == '-GETPROJECTSDATA-':
                try:
                    db = DBprovider.DBProvider("")
                    db.get_projects(cur)
                    window['-PROJDATARESULTS-'].update(" ", append=False)
                    window['-PROJDATARESULTS-'].update(str(db.projects).replace("),", "$\n"))
                    window['-PROJLIST-'].update(db.projectslist)
                except Exception as error:
                    sg.Popup('Ошибка', error.args)
            elif event == '-COPYPROJ-':
                try:
                    sg.Popup(f"Вы выбрали {values['-PROJLIST-'][0]}")
                    host = ip
                    user = UserLogin
                    secret = UserPassword
                    port = 22
                    db.getPathbyProj(cur,values['-PROJLIST-'][0])
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(hostname=host, username=user, password=secret, port=port)
                    pathToProject = str(db.projectpath).replace("[('","")
                    pathToProject = pathToProject[:-4]
                    #ssssss= f'git clone ssh://{user}@{host}{pathToProject}'
                    stdin, stdout, stderr = client.exec_command(f'git clone ssh://{user}@{host}{pathToProject}')
                    data = stdout.read() + stderr.read()
                    window['-SSHRESULT-'].update(data)
                    client.close()
                except Exception as error:
                    sg.Popup('', error.args)

            elif event == '-EXECPRIV-':
                try:
                    if values['-TABLESSETTINGSCOMBO-'][0] == "GRANT":
                        strrrr= (f"{values['-TABLESSETTINGSCOMBO-'][0]} "
                             f"{values['-TABLESPRIVCOMBO-'][0]} on "
                             f"{values['-TABLESCOMBO-'][0]} TO "
                             f"{values['-USERSCOMBO-'][0]};").replace("('","").replace("',)","")
                    else:
                        strrrr = (f"{values['-TABLESSETTINGSCOMBO-'][0]} "
                                  f"{values['-TABLESPRIVCOMBO-'][0]} ON "
                                  f"{values['-TABLESCOMBO-'][0]} FROM "
                                  f"{values['-USERSCOMBO-'][0]};").replace("('", "").replace("',)", "")
                    sg.Popup(strrrr)

                    db.prev_exec(cur,strrrr)
                    sg.Popup(db.execresult)


                except Exception as error:
                    sg.Popup('', error.args)

            elif event == '-USERCREATE-':
                try:
                    strtoexec = "create role "
                    strtoexec+= values['-NEWUSERNAME-']

                    if values['-SUPERUSER-CHECKBOX-']:
                        strtoexec+= " SUPERUSER"
                    else:
                        strtoexec += " NOSUPERUSER"

                    if values['-CreateDB-CHECKBOX-']:

                        strtoexec+= " CREATEDB"
                    else:
                        strtoexec += " NOCREATEDB"

                    if values['-CreateRole-CHECKBOX-']:
                        strtoexec+= " CREATEROLE"
                    else:
                        strtoexec += " NOCREATEROLE"

                    if values['-INHERIT-CHECKBOX-']:
                        strtoexec += " INHERIT"

                    if values['-LOGIN-CHECKBOX-']:
                        strtoexec += " LOGIN"

                    strtoexec+=";"
                    sg.popup(strtoexec)
                    db.usercreate(cur,strtoexec)
                    sg.Popup(db.execresult)



                except Exception as error:
                    sg.Popup('', error.args)




