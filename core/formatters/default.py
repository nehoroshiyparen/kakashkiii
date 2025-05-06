from .base import BaseFormatter

class DefaultFormatter(BaseFormatter):
    """Форматирование для вывода в файл/консоль *** файл на всякий случай"""
    def format_raw(self, data: str) -> str:
        return data
    
    def format_clipboard(self, data: str) -> str:
        return data