# app.py
from flask import Flask
from flask_socketio import SocketIO
from endpoints import api
from status import start_status_monitor, status_data
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api, url_prefix="/api")

# Initialize Flask-SocketIO (using eventlet for asynchronous support)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def on_connect():
    print("Client connected via WebSocket")

def background_status_thread():
    import time
    while True:
        # Emit the current status to all connected clients every 5 seconds.
        socketio.emit("status_update", status_data)
        time.sleep(5)

if __name__ == '__main__':
    start_status_monitor()  # Start monitoring status updates.
    socketio.start_background_task(target=background_status_thread)
    socketio.run(app, host="0.0.0.0", port=Config.API_PORT)
