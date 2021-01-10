import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm
import FaceIdentifier as fi

sidFilePath = ""
screenshotFilePath = ""
attendance = {}


def select_sid():
    global sidFilePath
    sidFilePath = tkf.askdirectory()


def select_screenshots():
    global screenshotFilePath
    screenshotFilePath = tkf.askdirectory()


def match_faces():
    global attendance
    if sidFilePath == "":
        tkm.showinfo("Error", "No Student ID folder selected")
        return
    if screenshotFilePath == "":
        tkm.showinfo("Error", "No Zoom Meeting screenshot folder selected")
        return
    face_identifier = fi.FaceIdentifier(sidFilePath, screenshotFilePath)
    attendance = face_identifier.recognize_faces()


root = tk.Tk()
root.title("placeholder text")
select_sid_button = tk.Button(root, text="Select Student ID Folder", command=select_sid)
select_screenshots_button = tk.Button(root, text="Select Zoom Meeting Screenshots Folder", command=select_screenshots)
generate_attendance_button = tk.Button(root, text="Generate Attendance", command=match_faces)

select_sid_button.pack()
select_screenshots_button.pack()
generate_attendance_button.pack()

tk.mainloop()