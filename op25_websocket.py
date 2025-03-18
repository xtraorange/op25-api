# app.py
import time
import json
from flask import Flask
from flask_socketio import SocketIO
from api import api
from config import Config


from op25_instance import op25   # Our OP25 state class.
from op25_journal_reader import OP25JournalReader  # Reads the systemd journal and updates op25.
from op25_websocket_notifier import OP25WebsocketNotifier  # Notifies websocket clients when op25 updates.

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api, url_prefix="/api")

# Initialize Flask-SocketIO (using eventlet for asynchronous support)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def on_connect():
    print("Client connected via WebSocket")


# Start the journal reader thread to update the op25 state.
journal_reader = OP25JournalReader(op25)
journal_reader.start()

# Initialize the websocket notifier.
notifier = OP25WebsocketNotifier(op25, socketio)

if __name__ == '__main__':
    # Run the Flask-SocketIO server.
    socketio.run(app, host="0.0.0.0", port=Config.API_PORT)
