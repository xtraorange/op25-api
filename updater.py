# updater.py
import os
import subprocess
import sys
from config import Config

def perform_update():
    """
    Performs a git pull based on UPDATE_MODE and then restarts the application.
    """
    update_mode = Config.UPDATE_MODE
    repo_dir = Config.REPO_DIR
    os.chdir(repo_dir)
    
    if update_mode == "dev":
        cmd = ["git", "pull"]
    else:
        # For production, you might implement logic to check out a specific release.
        cmd = ["git", "pull"]
    
    result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    restart_application()
    return result

def restart_application():
    """Restart the current Python process."""
    python = sys.executable
    os.execv(python, [python] + sys.argv)
