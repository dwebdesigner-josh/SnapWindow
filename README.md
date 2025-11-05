```
+------------------------------------------------------+
|                                                      |
|  ███████╗███╗   ██╗ █████╗ ██████╗                   |
|  ██╔════╝████╗  ██║██╔══██╗██╔══██╗                  |
|  ███████╗██╔██╗ ██║███████║██████╔╝                  |
|  ╚════██║██║╚██╗██║██╔══██║██╔═══╝                   |
|  ███████║██║ ╚████║██║  ██║██║                       |
|  ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝                       |
|                                                      |
|  ██╗    ██╗██╗███╗   ██╗██████╗  ██████╗ ██╗    ██╗  |
|  ██║    ██║██║████╗  ██║██╔══██╗██╔═══██╗██║    ██║  |
|  ██║ █╗ ██║██║██╔██╗ ██║██║  ██║██║   ██║██║ █╗ ██║  |
|  ██║███╗██║██║██║╚██╗██║██║  ██║██║   ██║██║███╗██║  |
|  ╚███╔███╔╝██║██║ ╚████║██████╔╝╚██████╔╝╚███╔███╔╝  |
|   ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝  ╚══╝╚══╝   |
|                                                      |
+------------------------------------------------------+
```
SnapWindow
*Only supports Windows and Chrome

Instructions: 
1. Make sure you have Python 3 installed with tkinter included (in Python 3 install process, select customize installation, and make sure tcl/tk are checked)
        a. WINDOWS if python 3 is already installed but you can't run the app/are missing tkinter, open Start Menu on Windows > Add/Remove Programs > Python 3.# > Modify > select tcl/tk > finish
3. Download zip file of repo and extract
4. cd to extract location
5. run Setup.bat then run SnapWindow.bat (can create shortcut for this on your desktop)
6. Open game/program/whatever you want to use as your main focus, make sure it is windowed borderless if it is a game.
7. Once you are ready to pull up the snap window, press the following on your keyboard:
     Ctrl Alt S
8. Choose a site to open from the options, or enter a website URL manually (https://www.example.com or example.com) and click Submit
9. Once you have found the video you want, press the following on your keyboard:
     Ctrl Alt F
     8. (a) To minimize or unminimize the Snap Window without ending the program, 
     press Ctrl Alt F again
     8. (b) Ff you want to navigate through the site to find another video after entering snap mode, simply drag to resize the site to a better size for navigating, then once you have found the next video, press Ctrl Alt F again to put it back in Snap size/positioning 
10. Once you are finished with the snap window, close it and end the SnapPlayer.py program with the following:
     Ctrl Alt E




NOTES FOR ALTERATION:

<> CHANGE POSITION <>

     To change positioning and size of snap window, conditional to youtube or nonyoutube windows, change the coordinates in the following lines in SnapPlayer.py:
               if "youtube.com" in snap_url:
               print(f"youtube url detected - repositioning to hide nav bar")
               win32gui.SetWindowPos(target, win32con.HWND_TOPMOST, 0, -200, 500, 450, 0) 
               else:
               print(f"non-youtube url detected - repositioning to fit video player")
               win32gui.SetWindowPos(target, win32con.HWND_TOPMOST, 0, -100, 500, 350, 0) 

          > COORDINATES: x, y, cx (left/right position), cy (up/down position), 0 (keep at zero) 

