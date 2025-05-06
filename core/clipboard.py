import pyperclip
import threading
from typing import Callable

class ClipboardMonitor:
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.active = False
        self.thread = None
        self.last_content = ""

    def start(self):
        """Запускает мониторинг буфера в отдельном потоке"""
        self.active = True
        self.thread = threading.Thread(target=self._monitor)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Останавливает мониторинг"""
        self.active = False
        if self.thread:
            self.thread.join()

    def _monitor(self):
        """Фоновая проверка буфера обмена"""
        while self.active:
            try:
                current = pyperclip.paste()
                if current != self.last_content and current.strip():
                    self.callback(f"[CLIPBOARD] {current}")
                    self.last_content = current
            except Exception:
                pass
            threading.Event().wait(1.0)

#    def handle_copy(self):
 #       """Обработка действия копирования"""
  #      try:
    #        content = pyperclip.paste()
   #         if content.strip():
     #           self.callback(f"[COPY] {content}")
      #  except Exception as e:
       #     self.callback(f"[CLIPBOARD COPY ERROR] {str(e)}")
    
    def handle_paste(self):
        """Обработка действия вставки"""
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content.strip():
                self.callback(f"\n[PASTE]: {clipboard_content}\n")
        except Exception as e:
            self.callback(f"[CLIPBOARD PASTE ERROR] {str(e)}")