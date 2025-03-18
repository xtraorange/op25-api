# endpoints.py
import os
from flask import Blueprint, request, jsonify
from updater import perform_update
from config import Config

api = Blueprint("api", __name__)

def authorize_request():
    token = request.headers.get("Authorization")
    return token == Config.SECRET_TOKEN

@api.route("/update", methods=["POST"])
def update():
    if not authorize_request():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        result = perform_update()
        return jsonify({"message": "Update successful", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/hold", methods=["POST"])
def hold():
    if not authorize_request():
        return jsonify({"error": "Unauthorized"}), 401
    from status import status_data
    status_data["hold_active"] = True
    return jsonify({"message": "Hold command executed", "hold_active": True}), 200

@api.route("/release_hold", methods=["POST"])
def release_hold():
    if not authorize_request():
        return jsonify({"error": "Unauthorized"}), 401
    from status import status_data
    status_data["hold_active"] = False
    return jsonify({"message": "Hold released", "hold_active": False}), 200

@api.route("/skip", methods=["POST"])
def skip():
    if not authorize_request():
        return jsonify({"error": "Unauthorized"}), 401
    from status import status_data
    status_data["active_tgid"] = None
    status_data["duration"] = 0
    return jsonify({"message": "Skip command executed"}), 200

@api.route("/whitelist", methods=["POST"])
def update_whitelist():
    if not authorize_request():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    tgids = data.get("tgids")
    if not tgids:
        return jsonify({"error": "No TGIDs provided"}), 400
    try:
        with open(Config.WHITELIST_FILE, "w") as f:
            for tgid in tgids:
                f.write(f"{tgid}\n")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Whitelist updated", "tgids": tgids}), 200

@api.route("/whitelist", methods=["GET"])
def get_whitelist():
    try:
        with open(Config.WHITELIST_FILE, "r") as f:
            tgids = [line.strip() for line in f if line.strip()]
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"whitelist": tgids}), 200

@api.route("/blacklist", methods=["POST"])
def update_blacklist():
    if not authorize_request():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    tgids = data.get("tgids")
    if not tgids:
        return jsonify({"error": "No TGIDs provided"}), 400
    try:
        with open(Config.BLACKLIST_FILE, "w") as f:
            for tgid in tgids:
                f.write(f"{tgid}\n")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Blacklist updated", "tgids": tgids}), 200

@api.route("/blacklist", methods=["GET"])
def get_blacklist():
    try:
        with open(Config.BLACKLIST_FILE, "r") as f:
            tgids = [line.strip() for line in f if line.strip()]
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"blacklist": tgids}), 200

@api.route("/talkgroups", methods=["GET"])
def get_talkgroups():
    try:
        tg_dict = {}
        with open(Config.TALKGROUPS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    tg_dict[parts[0]] = parts[1]
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"talkgroups": tg_dict}), 200

@api.route("/talkgroups", methods=["POST"])
def update_talkgroups():
    if not authorize_request():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    tg_dict = data.get("talkgroups")
    if not tg_dict or not isinstance(tg_dict, dict):
        return jsonify({"error": "Invalid talkgroups data"}), 400
    try:
        with open(Config.TALKGROUPS_FILE, "w") as f:
            for tgid, name in tg_dict.items():
                f.write(f"{tgid}\t{name}\n")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Talkgroups updated", "talkgroups": tg_dict}), 200

@api.route("/status", methods=["GET"])
def get_status():
    from status import status_data
    return jsonify(status_data), 200

@api.route("/logs", methods=["GET"])
def get_logs():
    try:
        with open(Config.LOG_FILE, "r") as f:
            lines = f.readlines()
            # Return last 100 lines
            log_output = "".join(lines[-100:])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"logs": log_output}), 200
