import PySimpleGUI as sg

class UI_LoginWindow():
    UserLogin = ''
    UserPassword = ''
    def __init__(self):
        menu_def = [['&File', ['&Open', '&Save', '&Properties', 'E&xit']],
                ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Toolbar', ['---','---', 'Command &3', 'Command &4']],
                ['&Help', '&About...'], ]

        layout = [[sg.Menu(menu_def,)],
        [sg.Text('Логин:', size=(15, 1)), sg.Input(size=(20, 1), key=('-Login-'))],
        [sg.Text('Пароль:', size=(15, 1)), sg.Input(size=(20, 1), key=('-Password-'),password_char='*')],
        [sg.Button('OK'), sg.Button('Exit')]]

        window = sg.Window('Форма входа', layout)

        while True:
            event, values = window.read()
    
            if event == 'OK':
                self.UserLogin = values['-Login-']
                self.UserPassword = values['-Password-']
                window.close()

            elif event == 'Exit' in event == sg.WIN_CLOSED:
                break   

            elif event == sg.WIN_CLOSED:
                break

        window.close()

