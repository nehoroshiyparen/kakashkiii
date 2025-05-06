from .base import BaseFormatter

class TelegramFormatter(BaseFormatter):
    def format_raw(self, raw: str, clean: str = "") -> str:
        return (
            "Raw: \n"
            f"```\n{raw}\n```\n"
            f"Clean: \n`{clean or 'no text'}`"
        )
    
    def format_clipboard(self, data: str) -> str:
        if not data:
            return "Пустой буфер"
            
        return data