import PySimpleGUI as sg
import sqlite3

class Subjects:
    def __init__(self):
        self.layout = [
            [sg.Text("ID"), sg.Push(), sg.InputText(key='id')],
            [sg.Text("Name"), sg.Push(), sg.InputText(key='name')],
            [sg.Text("Group1"), sg.Push(), sg.InputText(key='g1')],
            [sg.Text("Group2"), sg.Push(), sg.InputText(key='g2')],
            [sg.Text("Group3"), sg.Push(), sg.InputText(key='g3')],
            [sg.Button("Insert"), sg.Push(), sg.Button("Home"), sg.Button("View Subjects")],
        ]
        self.window = sg.Window("Subjects", self.layout)
    def run(self):
        while True:
            event, values = self.window.read()

            if event == "Insert":
                id = values['id']
                name = values['name']
                g1 = values['g1']
                g2 = values['g2']
                g3 = values['g3']

                conn = sqlite3.connect('records.db')
                print("connected")
                cursor = conn.cursor()
                try:
                    sql = '''INSERT INTO subjects(ID,Name,Group1, Group2, Group3)
                                 VALUES(?,?,?,?,?) '''
                    data = (id, name, g1, g2, g3)
                    cursor.execute(sql, data)
                    conn.commit()
                    sg.popup("Data Inserted Successfully !!")
                except Exception as e:
                    sg.popup(e)
                conn.close()

                self.window['id'].update('')
                self.window['name'].update('')
                self.window['g1'].update('')
                self.window['g2'].update('')
                self.window['g3'].update('')

                # print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
            elif event == "Home":
                from main import Home
                self.window.close()
                Home().run()
            elif event == "View Subjects":
                self.window.close()
                from viewsubjects import ViewSubjects
                ViewSubjects().run()

            elif event == sg.WINDOW_CLOSED:
                break

        self.window.close()

