import PySimpleGUI as sg
import sqlite3

class ViewData:
    def __init__(self):
        self.layout = [
            [sg.Table(values=self.connect(), headings=['ID', 'Name', 'Address'], auto_size_columns=True, num_rows=10,
                      key='table', enable_events=True)],
            [sg.Button('Exit'), sg.Button('Home'), sg.Button("Delete"), sg.Button("Update")]
        ]
        self.window = sg.Window("View Data", self.layout)
        self.selected_row = None

    def connect(self):
        try:
            conn = sqlite3.connect('records.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data
        except Exception as e:
            sg.PopupError("Error:", e)
            return []

    def delete_row(self, row_id):
        try:
            conn = sqlite3.connect("records.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE roll=?", (row_id,))
            conn.commit()
            cursor.close()
            conn.close()
            sg.popup("Data Deleted Successfully", font=('Helvetica', 20))
            self.window['table'].update(values=self.connect())
        except Exception as e:
            sg.PopupError("Error:", e)

    def update_row(self, row_id, updated_values):
        try:
            conn = sqlite3.connect("records.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET Name=?, Address=? WHERE roll=?",
                (updated_values['Name'], updated_values['Address'], row_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            sg.popup("Data Updated Successfully", font=('Helvetica', 20))
            self.window['table'].update(values=self.connect())
        except Exception as e:
            sg.PopupError("Error:", e)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == 'Exit' or event == sg.WINDOW_CLOSED:
                break
            elif event == 'Home':
                from main import Home  # Assuming you have a 'main.py' with Home class
                self.window.close()
                Home().run()
            elif event == 'Delete':
                selected_row = values['table']
                if not selected_row:
                    sg.PopupError("Please select a row to delete.")
                else:
                    row_id = self.connect()[selected_row[0]][0]  # Get ID of selected row
                    self.delete_row(row_id)
            elif event == 'Update':
                selected_row = values['table']
                if not selected_row:
                    sg.PopupError("Please select a row to update.")
                else:
                    row_data = self.connect()[selected_row[0]]
                    layout = [
                        [sg.Text("ID", font=('Helvetica', 20)), sg.Push(), sg.InputText(row_data[0], font=('Helvetica', 20), disabled=True)],
                        [sg.Text("Name", font=('Helvetica', 20)), sg.Push(), sg.InputText(row_data[1], key='Name', font=('Helvetica', 20))],
                        [sg.Text("Address", font=('Helvetica', 20)), sg.Push(), sg.InputText(row_data[2], key='Address', font=('Helvetica', 20))],
                        [sg.Push(), sg.Button("Update", font=('Helvetica', 20)), sg.Push(), sg.Button("Exit", key='close', font=('Helvetica', 20)), sg.Push()]
                    ]
                    update_window = sg.Window("Update Row", layout)
                    while True:
                        update_event, update_values = update_window.read()
                        if update_event == 'Update':
                            self.update_row(row_data[0], update_values)
                            break
                        elif update_event == 'close' or update_event == sg.WINDOW_CLOSED:
                            break
                    update_window.close()

        self.window.close()


