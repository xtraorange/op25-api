import time


class OP25WebsocketNotifier:
    """
    Registers a callback on an OP25 object so that whenever the object is updated,
    it emits an update via Flask-SocketIO.
    """
    def __init__(self, op25, socketio):
        """
        :param op25: An instance of your OP25 status class.
        :param socketio: The Flask-SocketIO instance.
        """
        self.op25 = op25
        self.socketio = socketio
        # Register our callback with the OP25 object.
        self.op25.register_callback(self.notify_update)

    def notify_update(self, prop, value):
        """
        Called when the OP25 object's property changes.
        Emits a "status_update" event via socketio with the updated value.
        
        :param prop: The property name that changed.
        :param value: The new value of the property.
        """
        update = {
            prop: value,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.socketio.emit("status_update", update)