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
    snap_url = url_entry.get()  # Get the URL directly from the entry widget
    time.sleep(1)

    root.destroy()

root = Tk()
root.title("Snap Window")
root.geometry("600x320")
root.attributes("-topmost", True)


url_entry_label = Label(root, text="Enter URL for snap window (without https://) or choose a site below")
url_entry_label.pack(pady=10)

url_entry = Entry(root)
url_entry.pack(pady=10)

button_frame = Frame(root)
button_frame.pack(pady=10)

netflix = Button(button_frame, text="Netflix", command=netflix)
netflix.grid(row=0, column=0, padx=10, pady=10)

hulu_button = Button(button_frame, text="Hulu", command=hulu)
hulu_button.grid(row=0, column=1, padx=10, pady=10)

youtube_button = Button(button_frame, text="Youtube", command=youtube)
youtube_button.grid(row=1, column=0, padx=10, pady=10)

disney_button = Button(button_frame, text="Disney+", command=disney)
disney_button.grid(row=1, column=1, padx=10, pady=10)


# Create a submit button
submit_button = Button(root, text="Submit", command=submit)
submit_button.pack(side=BOTTOM, pady=20)

runningstep1 = 1

while runningstep1==1:

        if (win32api.GetAsyncKeyState(win32con.VK_CONTROL) & 0x8000) and \
    (win32api.GetAsyncKeyState(win32con.VK_MENU) & 0x8000) and \
    (win32api.GetAsyncKeyState(ord('S')) & 0x8000):
            root.mainloop()
            runningstep1=0
            time.sleep(0.3)  # prevent multiple toggles


# ------------ LAUNCH URL IN APP MODE BROWSER ------------

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



snap_windows = None
try_count = 0

while not snap_windows:
    snap_windows = find_chrome_window_by_title()
    if snap_windows:
        target = snap_windows[0]
        print(f"Found Snap window: {target}")
    else:
        print("No Snap window found")
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
        win32gui.SetWindowPos(target, win32con.HWND_TOPMOST, 0, -200, 500, 450, 0) 


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
        win32gui.PostMessage(target, win32con.WM_CLOSE, 0, 0)
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







