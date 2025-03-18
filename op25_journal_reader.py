import time
import json
import threading
from systemd import journal

class OP25JournalReader(threading.Thread):
    """
    A thread that reads log entries from systemd's journal for op25.service
    and updates the provided op25 object accordingly.
    """
    def __init__(self, op25, poll_interval=1):
        """
        Initialize the journal reader.
        
        :param op25: An instance of your OP25 status class.
        :param poll_interval: How long to wait (in seconds) between checks for new log entries.
        """
        super().__init__(daemon=True)
        self.op25 = op25
        self.poll_interval = poll_interval
        self._running = True

    def parse_message(self, message):
        """
        Attempt to parse a journal message.
        First, try to decode it as JSON; if that fails, fall back to parsing key:value pairs.
        
        :param message: The log message string.
        :return: A dictionary of parsed values.
        """
        parsed = {}
        try:
            parsed = json.loads(message)
        except Exception:
            # Fallback: try to split the message into tokens of key:value.
            tokens = message.split()
            for token in tokens:
                if ":" in token:
                    key, value = token.split(":", 1)
                    parsed[key] = value
        return parsed

    def run(self):
        j = journal.Reader()
        j.add_match(_SYSTEMD_UNIT='op25.service')
        j.seek_tail()  # Start at the end to only get new entries
        
        while self._running:
            if j.wait(self.poll_interval * 1000):
                for entry in j:
                    message = entry.get("MESSAGE", "")
                    data = self.parse_message(message)
                    # Update the op25 object using the parsed data.
                    self.op25.update_from_dict(data)
            time.sleep(self.poll_interval)

    def stop(self):
        """Stop the journal reader thread."""
        self._running = False