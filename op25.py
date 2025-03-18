import time
import json

class OP25:
    def __init__(self):
        # Private attributes for state.
        self._active_tgid = None
        self._duration = 0
        self._hold_active = False
        self._last_update = None
        self._whitelist = []
        self._blacklist = []
        self._talkgroups = {}
        
        # List of callbacks: each callback will be called with (property_name, new_value)
        self._callbacks = []

    # Method to register a callback subscriber.
    def register_callback(self, callback):
        """Register a callback that will be called when a property changes.
           The callback should accept two arguments: property_name and new_value."""
        self._callbacks.append(callback)

    def _notify(self, prop, value):
        """Notify all registered callbacks that property `prop` has changed to `value`."""
        for cb in self._callbacks:
            try:
                cb(prop, value)
            except Exception as e:
                print(f"Callback error on {prop}: {e}")

    @property
    def active_tgid(self):
        return self._active_tgid

    @active_tgid.setter
    def active_tgid(self, value):
        if self._active_tgid != value:
            self._active_tgid = value
            self._notify("active_tgid", value)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if self._duration != value:
            self._duration = value
            self._notify("duration", value)

    @property
    def hold_active(self):
        return self._hold_active

    @hold_active.setter
    def hold_active(self, value):
        if self._hold_active != value:
            self._hold_active = value
            self._notify("hold_active", value)

    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, value):
        if self._last_update != value:
            self._last_update = value
            self._notify("last_update", value)

    @property
    def whitelist(self):
        return self._whitelist

    @whitelist.setter
    def whitelist(self, value):
        if self._whitelist != value:
            self._whitelist = value
            self._notify("whitelist", value)

    @property
    def blacklist(self):
        return self._blacklist

    @blacklist.setter
    def blacklist(self, value):
        if self._blacklist != value:
            self._blacklist = value
            self._notify("blacklist", value)

    @property
    def talkgroups(self):
        return self._talkgroups

    @talkgroups.setter
    def talkgroups(self, value):
        if self._talkgroups != value:
            self._talkgroups = value
            self._notify("talkgroups", value)

    def update_from_dict(self, data):
        """
        Update multiple properties at once from a dictionary.
        This is useful if you parse a JSON log entry or similar structured data.
        Expected keys: active_tgid, duration, hold_active, whitelist, blacklist, talkgroups
        """
        if "active_tgid" in data:
            self.active_tgid = data["active_tgid"]
        if "duration" in data:
            try:
                self.duration = int(data["duration"])
            except ValueError:
                pass
        if "hold_active" in data:
            # Interpret truthy values
            self.hold_active = str(data["hold_active"]).lower() in ["true", "1", "yes"]
        if "whitelist" in data:
            self.whitelist = data["whitelist"] if isinstance(data["whitelist"], list) else [data["whitelist"]]
        if "blacklist" in data:
            self.blacklist = data["blacklist"] if isinstance(data["blacklist"], list) else [data["blacklist"]]
        if "talkgroups" in data:
            self.talkgroups = data["talkgroups"]
        # Update the last update time on any change.
        self.last_update = time.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return json.dumps({
            "active_tgid": self.active_tgid,
            "duration": self.duration,
            "hold_active": self.hold_active,
            "last_update": self.last_update,
            "whitelist": self.whitelist,
            "blacklist": self.blacklist,
            "talkgroups": self.talkgroups,
        }, indent=2)