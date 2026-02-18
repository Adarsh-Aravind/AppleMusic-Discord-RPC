import subprocess
import os
import sys

def kill_process():
    print("Searching for Apple Music RPC processes...")
    try:
        # Use PowerShell to find processes with 'main.py' in the command line
        cmd = "Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -like '*main.py*' } | Select-Object -ExpandProperty ProcessId"
        result = subprocess.check_output(["powershell", "-Command", cmd], text=True)
        
        pids = [int(p) for p in result.splitlines() if p.strip()]
        
        if not pids:
            print("No running process found.")
            return

        print(f"Found {len(pids)} process(es). Terminating...")
        for pid in pids:
            try:
                # Iterate and kill
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, check=False)
                print(f"Killed PID {pid}")
            except Exception as e:
                print(f"Failed to kill {pid}: {e}")
                
        # Clean up PID file if it exists, just in case
        if os.path.exists("rpc.pid"):
            os.remove("rpc.pid")
            
    except Exception as e:
        print(f"Error during kill: {e}")
        # Fallback: simple taskkill of pythonw if main.py check fails
        os.system("taskkill /F /IM pythonw.exe")

if __name__ == "__main__":
    kill_process()
    print("Done.")
    import time
    time.sleep(1)
