import socket
from .base_handler import BaseOutputHandler

class TCPOutput(BaseOutputHandler):
    """Отправка данных через TCP сокет"""

    def __init__(self, host: str, port: int, timeout: float = 5.0):
        super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
    
    def send(self, data: str):
        try:
            if not self.socket:
                self._connect()

            self.socket.sendall(data.encode('utf-8'))
        except (socket.error, OSError) as e:
            self.logger.error(f"TCP send error: {e}")
            self._reconnect()
    
    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.host, self.port))

    def _reconnect(self):
        self.close()
        try:
            self._connect()
        except Exception as e:
            self.logger.error(f"Reconnect failed: {e}")
    
    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None