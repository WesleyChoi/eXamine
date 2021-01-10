import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm
import FaceIdentifier as fi

class Attendance(object):
    def __init__(self, attendanceDict):
        self.attendance = attendanceDict

    def showResults(self):
        # Creating tkinter window
        window = tk.Tk()

        style = ttk.Style()
        largeFontSize, smallFontSize = 15, 15
        style.configure("mystyle.Treeview", font=(None, smallFontSize), rowheight=int(smallFontSize*2))
        style.configure("mystyle.Treeview.Heading", font=(None, largeFontSize), rowheight=int(largeFontSize * 4))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        tree = ttk.Treeview(window, show='headings', style="mystyle.Treeview")
        tree['columns'] = ('Name', 'Attended')
        tree.column("Name", width=200)
        tree.column("Attended", width=150, anchor='c')
        tree.heading('Name', text="Name")
        tree.heading('Attended', text="Attended")

        counter = 0
        for name, attended in self.attendance.items():
            if attended:
                tree.insert("", "end", text=f'Line {counter}', values=(name, 'Yes'))
            else:
                tree.insert("", "end", text=f'Line {counter}', values=(name, 'No'))

        tree.pack()
        window.mainloop()

# How to use it
if __name__ == '__main__':
    attendanceDict = {'ONE PERSON': True, 'ANOTHER PERSON': False, 'THIRD PERSON': True}
    attendance = Attendance(attendanceDict)
    # Show the page
    attendance.showResults()