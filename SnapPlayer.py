import pyautogui
import time
import win32gui
import win32api
import win32con 
import win32process
import os
import shutil
import subprocess
import psutil
from thefuzz import process

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

# pre defined URL buttons
def netflix():
    global snap_url
    snap_url = "netflix.com"
    time.sleep(1)
    root.destroy()
def hulu():
    global snap_url
    snap_url = "hulu.com"
    time.sleep(1)
    root.destroy()
def youtube():
    global snap_url
    snap_url = "youtube.com"
    time.sleep(1)
    root.destroy()
def disney():
    global snap_url
    snap_url = "disneyplus.com"
    time.sleep(1)
    root.destroy()

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

fields = 'test','Enter URL (without https://):'

ents = makeform(root, fields)


disney_button = Button(root, text="Netflix", command=netflix)
disney_button.pack(side=TOP, pady=20)
disney_button = Button(root, text="Hulu", command=hulu)
disney_button.pack(side=TOP, pady=20)
disney_button = Button(root, text="Youtube", command=youtube)
disney_button.pack(side=TOP, pady=20)
disney_button = Button(root, text="Disney+", command=disney)
disney_button.pack(side=TOP, pady=20)

# Create a submit button
submit_button = Button(root, text="Submit", command=submit)
submit_button.pack(side=TOP, pady=20)


root.mainloop()


# ------------ LAUNCH YOUTUBE IN APP MODE BROWSER ------------

# append the windows file locations to list of paths in PATH os environment variable for shutil search 
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

keyword=snap_url


time.sleep(3)

window_titles = []

# Define a callback function to be called for each window
def enum_callback(hwnd, lParam):
    global window_titles
    # Get the window title
    window_title = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    
    try:
        process = psutil.Process(pid)  # Try to get the process
    except psutil.NoSuchProcess:
        # If the process doesn't exist, just skip this window
        return
    
    # Note the window handle and title for chrome or edge windows
    if window_title and (class_name == "Chrome_WidgetWin_1") and (process.name() == "chrome.exe"):
        window_titles.append(window_title)

# Call EnumWindows with the callback
win32gui.EnumWindows(enum_callback, None)


target_title = None
def choose_target():
    global target_title

    if window_titles:
        # Check the noted titles for one that matches the url entered   
        target_title= process.extractOne(f"{snap_url}", window_titles)[0]
        print(f"{target_title}")
    else:
        print("No window titles")


choose_target()


def find_chrome_window_by_title():
    hwnds = []
    def callback(hwnd, extra):
        class_name = win32gui.GetClassName(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        
        try:
            process = psutil.Process(pid)  # Try to get the process
        except psutil.NoSuchProcess:
            # If the process doesn't exist, just skip this window
            return
        
        title = win32gui.GetWindowText(hwnd)

        if title and (class_name == "Chrome_WidgetWin_1") and (process.name() == "chrome.exe") and title==target_title and win32gui.IsWindowVisible(hwnd):
                print(f"MATCH FOUND{title}")
                hwnds.append(hwnd)


    win32gui.EnumWindows(callback, None)
    return hwnds



youtube_windows = None
try_count = 0

while not youtube_windows:
    youtube_windows = find_chrome_window_by_title()
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







