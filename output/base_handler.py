from abc import ABC, abstractmethod
import logging

class BaseOutputHandler(ABC):
    """Абстрактный класс для всех обработчиков вывода"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def send(self, data: str):
        """Основной метод для отправки данных"""
        pass

    def close(self):
        """Корректное закрытие соединения"""
        pass