# status.py
import time
import threading

# Shared status data; in a real system this might be updated by parsing logs or op25 internals.
status_data = {
    "active_tgid": None,
    "duration": 0,
    "hold_active": False,
    "last_update": None,
    "whitelist": [],
    "blacklist": [],
    "talkgroups": {}
}

def monitor_status():
    """Simulate monitoring op25's status and update shared state."""
    import random
    while True:
        status_data["active_tgid"] = random.choice(["201", "202", "203", "204"])
        status_data["duration"] = random.randint(1, 120)
        status_data["hold_active"] = random.choice([True, False])
        status_data["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
        # Update whitelist
        try:
            with open("rpd_bcfy_wlist.tsv", "r") as f:
                status_data["whitelist"] = [line.strip() for line in f if line.strip()]
        except Exception:
            status_data["whitelist"] = []
        # Update blacklist
        try:
            with open("blacklist.tsv", "r") as f:
                status_data["blacklist"] = [line.strip() for line in f if line.strip()]
        except Exception:
            status_data["blacklist"] = []
        # Update talkgroups mapping
        try:
            tg_dict = {}
            with open("tgid_tags.tsv", "r") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) >= 2:
                        tg_dict[parts[0]] = parts[1]
            status_data["talkgroups"] = tg_dict
        except Exception:
            status_data["talkgroups"] = {}
        time.sleep(5)

def start_status_monitor():
    t = threading.Thread(target=monitor_status, daemon=True)
    t.start()
