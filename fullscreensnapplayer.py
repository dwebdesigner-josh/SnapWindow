import pyautogui
import time
import win32gui
import win32api
import win32con 

import keyboard

running=1

toggle = 0

original_rect = None

def find_chrome_window_by_title(keyword="YouTube"):
    hwnds = []

    def callback(hwnd, extra):
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        # Chrome windows usually have class starting with 'Chrome' and are visible
        if class_name.startswith("Chrome") and keyword in title and win32gui.IsWindowVisible(hwnd):
            hwnds.append(hwnd)

    win32gui.EnumWindows(callback, None)
    return hwnds

# Example usage
youtube_windows = find_chrome_window_by_title("YouTube")
if youtube_windows:
    target = youtube_windows[0]
    print(f"Found YouTube Chrome window: {target}")
else:
    print("No YouTube window found")


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







