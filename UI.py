import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm
import FaceIdentifier as fi

sidFilePath = ""
screenshotFilePath = ""
attendance = {}

buttonSize = (300, 100)
buttonPadding = (5, 5)

def select_sid():
    global sidFilePath
    sidFilePath = tkf.askdirectory()


def select_screenshots():
    global screenshotFilePath
    screenshotFilePath = tkf.askdirectory()


def generate_attendance():
    global attendance
    if sidFilePath == "":
        tkm.showinfo("Error", "No Student ID folder selected")
        return
    if screenshotFilePath == "":
        tkm.showinfo("Error", "No Zoom Meeting screenshot folder selected")
        return
    face_identifier = fi.FaceIdentifier(sidFilePath, screenshotFilePath)
    attendance = face_identifier.recognize_faces()

# Create main window
root = tk.Tk()
root.geometry("310x320")
root.title("eXamine")
root.configure(background="#e2e2e2")
icon = tk.PhotoImage(file='icon.png')
root.iconphoto(False, icon)

# Create UI elements
select_sid_button = tk.Button(root, text="Select Student ID Folder", command=select_sid)
select_screenshots_button = tk.Button(root, text="Select Zoom Meeting Screenshots Folder", command=select_screenshots)
generate_attendance_button = tk.Button(root, text="Generate Attendance", command=generate_attendance)

# Format
pixel = tk.PhotoImage(width = 1, height = 1)
select_sid_button.config(image = pixel, width = buttonSize[0] - 6, height = buttonSize[1] - 6, compound = "c", bg = "#73c2fb", padx=0, pady=0)
select_screenshots_button.config(image = pixel, width = buttonSize[0] - 6, height = buttonSize[1] - 6, compound = "c", bg = "#73c2fb", padx=0, pady=0)
generate_attendance_button.config(image = pixel, width = buttonSize[0] - 6, height = buttonSize[1] - 6, compound = "c", bg = "#73c2fb", padx=0, pady=0)

select_sid_button.config(font=("Proxima Nova", 15))
select_screenshots_button.config(font=("Proxima Nova", 15), wraplength=220)
generate_attendance_button.config(font=("Proxima Nova", 15))

# Place onto screen
select_sid_button.pack()
select_screenshots_button.pack()
generate_attendance_button.pack()

select_sid_button.place(x=buttonPadding[0], y=buttonPadding[1])
select_screenshots_button.place(x=buttonPadding[0], y=buttonPadding[1] * 2 + buttonSize[1])
generate_attendance_button.place(x=buttonPadding[0], y=buttonPadding[1] * 3 + buttonSize[1] * 2)

tk.mainloop()
