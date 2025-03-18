# config.py
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    SECRET_TOKEN = os.getenv("SECRET_TOKEN", "your-secret-token")
    HTTP_OR_HTTPS = os.getenv("HTTP_OR_HTTPS", "http")
    API_PORT = int(os.getenv("API_PORT", 8081))
    CONTROL_PORT = int(os.getenv("CONTROL_PORT", 23450))
    UPDATE_MODE = os.getenv("UPDATE_MODE", "dev")
    WHITELIST_FILE = os.getenv("WHITELIST_FILE", "rpd_bcfy_wlist.tsv")
    BLACKLIST_FILE = os.getenv("BLACKLIST_FILE", "blacklist.tsv")
    TALKGROUPS_FILE = os.getenv("TALKGROUPS_FILE", "tgid_tags.tsv")
    LOG_FILE = os.getenv("LOG_FILE", "op25.log")
    
    # Dynamically determine the repository directory as the parent directory of this file.
    REPO_DIR = os.getenv("REPO_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    
    # Determine GitHub repository URL from environment, or else use git config.
    _git_repo = os.getenv("GITHUB_REPO")
    if _git_repo:
        GITHUB_REPO = _git_repo
    else:
        try:
            GITHUB_REPO = subprocess.check_output(["git", "config", "--get", "remote.origin.url"],
                                                    cwd=REPO_DIR).decode("utf-8").strip()
        except Exception:
            GITHUB_REPO = "unknown"
