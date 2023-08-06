from socketIO_client_nexus import SocketIO
from json import load
from urllib2 import urlopen

class PostQuick:
    socket = None

    def __init__(self, key):
        self.socket = SocketIO(
            'postquick.startnet.co',
            80,
            params={
                'key': key,
                'ip': load(urlopen('https://api.ipify.org/?format=json'))['ip']
            }
        )

    def on(self, eventName, eventCallback):
        self.socket.on(eventName, eventCallback)

    def emit(self, eventName, eventValue):
        self.socket.emit(eventName, eventValue)
