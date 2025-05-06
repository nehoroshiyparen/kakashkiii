import telebot
from .base_handler import BaseOutputHandler
from typing import Optional

class TelegramOutput(BaseOutputHandler):
    """Отправка данных через Telegram бота"""
    def __init__(self, token: str, chat_id: str, parse_mode: Optional[str] = None):
        super().__init__()
        self.bot = telebot.TeleBot(token)
        self.chat_id = chat_id
        self.parse_mode = parse_mode
        self._check_connetction()

    def _check_connetction(self):
        try:
            self.bot.get_me()
        except Exception as e:
            self.logger.error(f"Telegram connection error: {e}")
    
    def send(self, data: str):
        try:
            # Отправка с форматированием в зависимости от типа данных
            if data.startswith("[PASTE]"):
                self.bot.send_message(
                    self.chat_id,
                    f"\n{data}",
                    parse_mode=self.parse_mode
                )
            elif data.startswith("[COPY]"):
                self.bot.send_message(
                    self.chat_id,
                    f"\n{data}",
                    parse_mode=self.parse_mode
                )
            else:
                self.bot.send_message(
                    self.chat_id,
                    f"{data}",
                    parse_mode=self.parse_mode
                )
        except Exception as e:
            print(f"Telegram send error: {e}")