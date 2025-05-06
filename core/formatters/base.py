from abc import  ABC, abstractmethod

class BaseFormatter(ABC):
    """Абстрактный базовый класс для всех форматтеров"""
    @abstractmethod
    def format_raw(self, data: str) -> str:
        pass

    @abstractmethod
    def format_clipboard(self, data: str) -> str:
        """Форматирование буфера обмена"""
        pass