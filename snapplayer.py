import pyautogui
import time
import win32gui
import win32con 

import keyboard


toggle = 0

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
    win32gui.ShowWindow(target, win32con.SW_RESTORE)
    win32gui.SetWindowPos(target, win32con.HWND_TOPMOST, 200, 200, 400, 600, 0) 

def overlay_off():
    win32gui.SetWindowPos(target, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
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
    if toggle==1:
        toggle = 0
        print(f"toggle set to {toggle}")
        overlay_off()
    print("Exiting script")

keyboard.add_hotkey('ctrl+alt+f', toggle_overlay)
keyboard.add_hotkey('ctrl+alt+e', end)


keyboard.wait('ctrl+alt+e')


# starttime = 5

# # Safety delay before starting
# print(f"Starting in {starttime} seconds... Move your mouse where needed.")
# time.sleep(starttime)




