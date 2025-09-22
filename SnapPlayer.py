import pyautogui
import time
import win32gui
import win32api
import win32con 
import os
import shutil
import subprocess

from tkinter import *
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
from tkinter import messagebox


def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=25, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries


def submit():
    global snap_url
    # Loop through the fields and retrieve the values from the Entry widgets
    user_inputs = {}
    for field, entry in ents:
        user_inputs[field] = entry.get()

    # Get the input data (for example, the 'Enter URL:' field)
    snap_url = user_inputs['Enter URL (without https://):']

    
    time.sleep(1)

    root.destroy()

root = Tk()
root.title("Snap Window")
root.geometry("600x320")
root.attributes("-topmost", True)

fields = 'Choose a site:', 'Enter URL (without https://):'

ents = makeform(root, fields)


# Create a submit button
submit_button = Button(root, text="Submit", command=submit)
submit_button.pack(side=TOP, pady=20)


root.mainloop()


# ------------ LAUNCH YOUTUBE IN APP MODE BROWSER ------------

# append the windows file locations to list of paths in PATH os environment variable for shutil search 
# (shouldn't need this append on linux)
os.environ['PATH'] += os.pathsep + r"C:\Program Files\Google\Chrome\Application"
os.environ['PATH'] += os.pathsep + r"C:\Program Files (x86)\Microsoft\Edge\Application"
# os.environ['PATH'] += os.pathsep + r"C:\Program Files\Mozilla Firefox"
#   removed as firefox doesn't support --app mode (nav bar removed from UI)

browser = shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("msedge")

print(f"{browser}")

if not browser:
    raise RuntimeError("Could not find web browser")

url=f"https://{snap_url}"

print(f"{url}")

subprocess.Popen([browser, f"--app={url}"])

# ------------------ INITIALIZE SNAP MODE ------------------

running = 1

toggle = 0

original_rect = None

def find_chrome_window_by_title(keyword="YouTube"):
    hwnds = []

    def callback(hwnd, extra):
        title = win32gui.GetWindowText(hwnd)
        # find window with Youtube in title
        if keyword in title and win32gui.IsWindowVisible(hwnd):
            hwnds.append(hwnd)

    win32gui.EnumWindows(callback, None)
    return hwnds

youtube_windows = None
try_count = 0

while not youtube_windows:
    youtube_windows = find_chrome_window_by_title("YouTube")
    if youtube_windows:
        target = youtube_windows[0]
        print(f"Found YouTube Chrome window: {target}")
    else:
        print("No YouTube window found")
    time.sleep(1)
    try_count += 1
    if try_count == 10:
        print("No snap window found")
        break


def overlay_on():
    global original_rect
    if target:
        original_rect = win32gui.GetWindowRect(target)

        win32gui.ShowWindow(target, win32con.SW_SHOWNORMAL)
        win32gui.ShowWindow(target, win32con.SW_RESTORE)
        win32gui.SetWindowPos(target, win32con.HWND_TOPMOST, 0, -275, 400, 600, 0) 

def overlay_off():
    if target:
        left, top, right, bottom = original_rect
        width = right - left
        height = bottom - top
        win32gui.SetWindowPos(target, win32con.HWND_NOTOPMOST, left, top, width, height,
                                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.ShowWindow(target, win32con.SW_MINIMIZE)


def toggle_overlay():
    global toggle
    if toggle==0:
        toggle = 1
        print(f"toggle set to {toggle}")
        overlay_on()
    else:
        toggle = 0
        print(f"toggle set to {toggle}")
        overlay_off()


def end():
    global toggle
    global running
    if toggle==1:
        toggle = 0
        print(f"toggle set to {toggle}")
        overlay_off()
    print("Exiting script")
    running=0
try:
    while running==1:
        
        if (win32api.GetAsyncKeyState(win32con.VK_CONTROL) & 0x8000) and \
    (win32api.GetAsyncKeyState(win32con.VK_MENU) & 0x8000) and \
    (win32api.GetAsyncKeyState(ord('F')) & 0x8000):
            toggle_overlay()
            time.sleep(0.3)  # prevent multiple toggles

        if (win32api.GetAsyncKeyState(win32con.VK_CONTROL) & 0x8000) and \
    (win32api.GetAsyncKeyState(win32con.VK_MENU) & 0x8000) and \
    (win32api.GetAsyncKeyState(ord('E')) & 0x8000):
            end()
            time.sleep(0.3)  # prevent multiple toggles
finally:
    end()







