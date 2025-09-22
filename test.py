import os
import shutil
import subprocess

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

url="https://www.youtube.com/watch?v=z2WlmQDzXwk"

subprocess.Popen([browser, f"--app={url}"])