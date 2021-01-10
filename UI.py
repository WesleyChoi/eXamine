import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm
import FaceIdentifier as fId
import PIL.ImageTk as imTk
import PIL.Image as im
import AttendanceUI

import os

sidFilePath = ""
screenshotFilePath = ""
attendance = {}

loading_bar_division = 1
current_progress = 0

windowSize = (310, 630)
buttonSize = (300, 100)
buttonPadding = (5, 5)

progress_bar : ttk.Progressbar = None
load_window : tk.Tk = None

face_identifier: fId.FaceIdentifier = None


def select_sid():
    global sidFilePath
    sidFilePath = tkf.askdirectory()


def select_screenshots():
    global screenshotFilePath
    screenshotFilePath = tkf.askdirectory()


def display_attendance():
    attendanceui = AttendanceUI.Attendance(attendance)
    attendanceui.showResults()


def visualize():
    face_identifier.zoomRecognize.showImages()


def create_loading_bar():
    global load_window, progress_bar
    load_window = tk.Tk()

    # load_logo_im: im.Image = im.open("Bottom Icon.PNG")
    # load_logo_im = load_logo_im.resize(buttonSize, im.ANTIALIAS)
    # load_logo = imTk.PhotoImage(load_logo_im)
    # load_logo_label = tk.Label(load_window, image=load_logo)

    progress_bar = ttk.Progressbar(load_window, orient=tk.HORIZONTAL, length=100, mode='determinate')

    # load_logo_label.pack()
    progress_bar.pack()

    load_window.mainloop()


def generate_attendance():
    global attendance, loading_bar_division, face_identifier
    if sidFilePath == "":
        tkm.showinfo("Error", "No Student ID folder selected")
        return
    if screenshotFilePath == "":
        tkm.showinfo("Error", "No Zoom Meeting screenshot folder selected")
        return
    if not os.listdir(sidFilePath):
        tkm.showinfo("Error", "Student ID folder is empty")
    if not os.listdir(screenshotFilePath):
        tkm.showinfo("Error", "Zoom Meeting screenshot folder is empty")

    display_images_button["state"] = "disabled"
    display_attendance_button["state"] = "disabled"

    loading_bar_division = len(os.listdir(sidFilePath)) + len(os.listdir(sidFilePath))
    face_identifier = fId.FaceIdentifier(sidFilePath, screenshotFilePath)

    # create_loading_bar()
    attendance = face_identifier.recognize_faces()

    display_images_button["state"] = "normal"
    display_attendance_button["state"] = "normal"


def progress_loading_bar():
    global progress_bar, load_window, current_progress
    progress_bar['value'] = current_progress * 100 / loading_bar_division
    load_window.update_idletasks()
    if current_progress == loading_bar_division:
        load_window.destroy()


# Create main window
root = tk.Tk()
root.geometry("%dx%d+%d+%d" % (windowSize[0], windowSize[1], (root.winfo_screenwidth() - windowSize[0]) / 2, (root.winfo_screenheight() - windowSize[1]) / 2))
root.title("eXamine")
root.configure(background="#e2e2e2")
icon = tk.PhotoImage(file='icon.png')
root.iconphoto(False, icon)

# Create UI elements
select_sid_button = tk.Button(root, text="Select Student ID Folder", command=select_sid)
select_screenshots_button = tk.Button(root, text="Select Zoom Meeting Screenshots Folder", command=select_screenshots)
generate_attendance_button = tk.Button(root, text="Generate Attendance", command=generate_attendance)
display_attendance_button = tk.Button(root, text="Display Attendance", command=display_attendance)
display_images_button = tk.Button(root, text="Visualize", command=visualize)
display_attendance_button["state"] = "disabled"
display_images_button["state"] = "disabled"

# Format
pixel = tk.PhotoImage(width = 1, height = 1)
select_sid_button.config(image = pixel, width = buttonSize[0] - 6, height = buttonSize[1] - 6, compound = "c", bg = "#73c2fb", padx=0, pady=0)
select_screenshots_button.config(image = pixel, width = buttonSize[0] - 6, height = buttonSize[1] - 6, compound = "c", bg = "#73c2fb", padx=0, pady=0)
generate_attendance_button.config(image = pixel, width = buttonSize[0] - 6, height = buttonSize[1] - 6, compound = "c", bg = "#73c2fb", padx=0, pady=0)
display_attendance_button.config(image = pixel, width = buttonSize[0] - 6, height = buttonSize[1] - 6, compound = "c", bg = "#73c2fb", padx=0, pady=0)
display_images_button.config(image = pixel, width = buttonSize[0] - 6, height = buttonSize[1] - 6, compound = "c", bg = "#73c2fb", padx=0, pady=0)

select_sid_button.config(font=("Proxima Nova", 15))
select_screenshots_button.config(font=("Proxima Nova", 15), wraplength=220)
generate_attendance_button.config(font=("Proxima Nova", 15))
display_attendance_button.config(font=("Proxima Nova", 15))
display_images_button.config(font=("Proxima Nova", 15))

image: im.Image = im.open("Bottom Icon.PNG")
image = image.resize(buttonSize, im.ANTIALIAS)
img = imTk.PhotoImage(image)
img_label = tk.Label(root, image=img)


# Place onto screen
select_sid_button.pack()
select_screenshots_button.pack()
generate_attendance_button.pack()
display_attendance_button.pack()
display_images_button.pack()

select_sid_button.place(x=buttonPadding[0], y=buttonPadding[1])
select_screenshots_button.place(x=buttonPadding[0], y=buttonPadding[1] * 2 + buttonSize[1])
generate_attendance_button.place(x=buttonPadding[0], y=buttonPadding[1] * 3 + buttonSize[1] * 2)
display_attendance_button.place(x=buttonPadding[0], y=buttonPadding[1] * 4 + buttonSize[1] * 3)
display_images_button.place(x=buttonPadding[0], y=buttonPadding[1] * 5 + buttonSize[1] * 4)
img_label.place(x=buttonPadding[0], y=buttonPadding[1] * 6 + buttonSize[1] * 5)

# Main loop
tk.mainloop()
