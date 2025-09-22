from thefuzz import process
import win32gui
import win32process
import psutil

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
    if window_title and class_name == "Chrome_WidgetWin_1" and (process.name() == "chrome.exe" or process.name() == "msedge.exe"):
        window_titles.append(window_title)

    # Call EnumWindows with the callback
    win32gui.EnumWindows(enum_callback, None)


if window_titles:
    # Check the noted titles for one that matches the url entered   
    target_title={process.extractOne("disneyplus.com", window_titles)}


def find_chrome_window_by_title():
    hwnds = []
    def callback(hwnd, extra):
        global target_title
        title = win32gui.GetWindowText(hwnd)
        
        # find window with Youtube in title
        if title==target_title and win32gui.IsWindowVisible(hwnd):
                hwnds.append(hwnd)

    win32gui.EnumWindows(callback, None)
    return hwnds


find_chrome_window_by_title()