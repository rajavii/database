import PySimpleGUI as sg
import sqlite3


class Home:
    def __init__(self):
        self.layout = [
            [sg.Text("Roll"), sg.Push(), sg.InputText(key='roll')],
            [sg.Text("Name"), sg.Push(), sg.InputText(key='name')],
            [sg.Text("Address"), sg.Push(), sg.InputText(key='address')],
            [sg.Button("Insert"), sg.Push(), sg.Button("Exit")],
            [sg.Button("Subjects"), sg.Button("View Data")]

        ]
        self.window = sg.Window("Home", self.layout)

    def run(self):
        while True:
            event, values = self.window.read()

            if event == "Insert":
                roll = values['roll']
                name = values['name']
                address = values['address']
                conn = sqlite3.connect('records.db')
                print("connected")
                cursor = conn.cursor()
                try:
                    sql = '''INSERT INTO students(roll,name,address)
                                 VALUES(?,?,?) '''
                    data = (roll, name, address)
                    cursor.execute(sql, data)
                    conn.commit()
                    sg.popup("Data Inserted Successfully !!")
                except Exception as e:
                    sg.popup(e)
                conn.close()

                self.window['roll'].update('')
                self.window['name'].update('')
                self.window['address'].update('')
                # print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
            elif event == "Exit":
                break
            elif event == "Subjects":
                self.window.close()
                from subjects import Subjects
                Subjects().run()
            elif event == "View Data":
                self.window.close()
                from viewdata import ViewData
                ViewData().run()
            elif event == sg.WINDOW_CLOSED:
                break

        self.window.close()


if __name__ == "__main__":
    Home().run()
