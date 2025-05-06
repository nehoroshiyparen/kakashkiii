from pynput import keyboard

special_keys = {
    keyboard.Key.space: ('␣', ' '),
    keyboard.Key.enter: ('↵', '\n'),
    keyboard.Key.tab: ('⇥', '\t'),
    keyboard.Key.backspace: ('⌫', '\b'),
    keyboard.Key.esc: ('⎋', None),
    keyboard.Key.shift: ('⇧', None),
    keyboard.Key.ctrl_l: ('^', None),
    keyboard.Key.ctrl_r: ('^', None),
    keyboard.Key.alt: ('⌥', None),
    keyboard.Key.cmd: ('⌘', None),
    keyboard.Key.caps_lock: ('⇪', None),
    keyboard.Key.f1: ('F1', None),
    keyboard.Key.f12: ('F12', None)
}