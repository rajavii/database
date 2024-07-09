import PySimpleGUI as sg
import sqlite3


class ViewSubjects:
    def __init__(self):
        self.layout = [
            [sg.Table(values=self.connect(), headings=['ID', 'Name', 'Group1', 'Group2', 'Group3'], auto_size_columns=False, num_rows=10,
                      key='table')],
            [sg.Button('Exit'), sg.Button('Home'), sg.Button('Delete'), sg.Button('Update')]
        ]
        self.window = sg.Window("View Data", self.layout)

    def connect(self):
        try:
            conn = sqlite3.connect('records.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects")
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            sg.Popup("error is", e)

    def delete_row(self, row_id):
        try:
            conn = sqlite3.connect("records.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subjects WHERE ID=?", (row_id,))
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
                "UPDATE subjects SET Name=?, Group1=?, Group2=?, Group3=? WHERE ID=?",
                (updated_values['Name'], updated_values['Group1'], updated_values['Group2'], updated_values['Group3'], row_id)
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
                    row_id = self.connect()[selected_row[0]]
                    layout = [
                        [sg.Text("ID", font=('Helvetica', 20)), sg.Push(), sg.InputText(row_id[0], font=('Helvetica', 20), disabled=True)],
                        [sg.Text("Name", font=('Helvetica', 20)), sg.Push(), sg.InputText(row_id[1], key='Name', font=('Helvetica', 20))],
                        [sg.Text("Group1", font=('Helvetica', 20)), sg.Push(), sg.InputText(row_id[2], key='Group1', font=('Helvetica', 20))],
                        [sg.Text("Group2", font=('Helvetica', 20)), sg.Push(), sg.InputText(row_id[3], key='Group2', font=('Helvetica', 20))],
                        [sg.Text("Group3", font=('Helvetica', 20)), sg.Push(),sg.InputText(row_id[4], key='Group3', font=('Helvetica', 20))],
                        [sg.Push(), sg.Button("Update", font=('Helvetica', 20)), sg.Push(), sg.Button("Exit", key='close', font=('Helvetica', 20)), sg.Push()]
                    ]
                    update_window = sg.Window("Update Row", layout)
                    while True:
                        update_event, update_values = update_window.read()
                        if update_event == 'Update':
                            self.update_row(row_id[0], update_values)
                            break
                        elif update_event == 'close' or update_event == sg.WINDOW_CLOSED:
                            break
                    update_window.close()
            if event == 'Home':
                from main import Home
                self.window.close()
                Home().run()
            self.window.close()


