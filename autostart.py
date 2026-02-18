import winreg
import sys
import os
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_to_startup():
    # Path to the python executable
    python_exe = sys.executable
    # Use pythonw.exe to run without console if possible, otherwise just python.exe
    # Assuming standard install, pythonw is in the same dir.
    pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
    if not os.path.exists(pythonw_exe):
        pythonw_exe = python_exe

    script_path = os.path.abspath("main.py")
    
    # Key path
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "AppleMusicRPC"
    
    # Command: "path/to/pythonw.exe" "path/to/main.py"
    command = f'"{pythonw_exe}" "{script_path}"'
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        print(f"Successfully added {app_name} to startup.")
        print(f"Command: {command}")
    except Exception as e:
        print(f"Failed to add to startup: {e}")

if __name__ == "__main__":
    add_to_startup()
    print("You can close this window.")
    input("Press Enter to exit...")
