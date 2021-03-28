import PySimpleGUI as sg

class UI_LoginWindow():
    UserLogin = ''
    UserPassword = ''
    def __init__(self):
        menu_def = [['&File', ['&Open', '&Save', '&Properties', 'E&xit']],
                ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Toolbar', ['---','---', 'Command &3', 'Command &4']],
                ['&Help', '&About...'], ]

        column_to_be_centered = [[sg.Menu(menu_def,)],
        [sg.Text('Логин:', size=(15, 1)), sg.Input(size=(20, 1),default_text=('adminuser'), key=('-Login-'))],
        [sg.Text('Пароль:', size=(15, 1)), sg.Input(size=(20, 1),default_text=('password'), key=('-Password-'), password_char='*')],
        [sg.Button('OK'), sg.Button('Exit')]]


        layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
                  [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
                   sg.Column(column_to_be_centered, vertical_alignment='center', justification='center', k='-C-')]]

        window = sg.Window('Window Title', layout, resizable=True, finalize=True)
        window['-C-'].expand(True, True, True)
        window['-EXPAND-'].expand(True, True, True)
        window['-EXPAND2-'].expand(True, False, True)

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

