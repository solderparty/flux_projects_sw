# Based on:
#  https://github.com/adafruit/Adafruit_CircuitPython_MacroPad/blob/main/adafruit_macropad.py Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#  https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Macropad_Hotkeys/code.py Copyright (c) 2021 Phillip Burgess for Adafruit Industries

import digitalio
import displayio
import keypad
import neopixel
import os
import terminalio
import usb_hid

import rp2040_stamp_macropad_board as board
from adafruit_debouncer import Debouncer
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse


class App:
    def __init__(self, macropad, data):
        self.name = data['name']
        self.macros = data['macros']
        self._macropad = macropad

    def switch(self):
        self._macropad.title = self.name + ' (' + str(self._macropad.app_index + 1) + '/' + str(len(self._macropad.apps)) + ')'

        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                self._macropad.set_pixel(i, self.macros[i][0])
                self._macropad.set_text(i, self.macros[i][1])
            else:  # Key not in use, no label or LED
                self._macropad.set_pixel(i, 0)
                self._macropad.set_text(i, '')


class MacroPad:
    def __init__(self, app_dir):
        key_pins = [ getattr(board, "KEY%d" % i) for i in range(1, 13) ]
        key_pins.append(board.BTN_CENTER)

        self._keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)
        self._pixels = neopixel.NeoPixel(board.NEOPIXEL, 12, brightness=0.5)

        self._btns = []
        for pin in [ board.BTN_LEFT, board.BTN_RIGHT ]: # board.BTN_CENTER
            io = digitalio.DigitalInOut(pin)
            io.switch_to_input(pull=digitalio.Pull.UP)
            self._btns.append(Debouncer(io))

        # Keyboard
        self._keyboard = Keyboard(usb_hid.devices)
        self._keyboard_layout = KeyboardLayoutUS(self._keyboard)
        self._consumer_control = ConsumerControl(usb_hid.devices)
        self._mouse = Mouse(usb_hid.devices)

        # UI
        self._group = None
        self._title_label = None
        self._init_ui()

        # Apps
        self._apps = []
        self._app_idx = 0
        self._load_apps(app_dir)

        if not self._apps:
            self._title_label.text = 'NO APPS FOUND'

    def _init_ui(self):
        w = board.DISPLAY.width // 3 - 1
        h = board.DISPLAY.height // 5

        self._group = displayio.Group()

        for y in range(4):
            for x in range(3):
                self._group.append(label.Label(terminalio.FONT, text='test', color=0xffffff, anchor_point=(x / 2, 1.0), anchored_position=((board.DISPLAY.width - 1) * x / 2, (y + 2) * h + 2)))

        self._group.append(Rect(0, 0, board.DISPLAY.width, h, fill=0xffffff))

        self._title_label = label.Label(terminalio.FONT, text='Title', color=0x000000, anchor_point=(0.5, 0.0), anchored_position=(board.DISPLAY.width // 2, -2))
        self._group.append(self._title_label)

        board.DISPLAY.show(self._group)

    def _load_apps(self, app_dir):
        files = os.listdir(app_dir)
        files.sort()

        for filename in files:
            if filename.endswith('.py'):
                try:
                    module = __import__(app_dir + '/' + filename[:-3])
                    self._apps.append(App(self, module.app))
                except (SyntaxError, ImportError, AttributeError, KeyError, NameError, IndexError, TypeError) as err:
                    import traceback
                    print('ERROR in', filename)
                    traceback.print_exception(err, err, err.__traceback__)

    @property
    def apps(self):
        return self._apps

    @property
    def title(self):
        return self._title_label.text

    @title.setter
    def title(self, title):
        self._title_label.text = title

    @property
    def app_index(self):
        return self._app_idx

    def text(self, i):
        return self._group[i]

    def set_text(self, i, text):
        self._group[i].text = text

    def pixel(self, i):
        return self._pixels[i]

    def set_pixel(self, i, pixel):
        mapping = [9, 10, 11, 8, 7, 6, 3, 4, 5, 2, 1, 0]

        self._pixels[mapping[i]] = pixel

    def update(self):
        for btn in self._btns:
            btn.update()

        # Left Button
        if self._btns[0].fell:
            self._app_idx = (self._app_idx - 1) % len(self._apps)
            self._apps[self._app_idx].switch()

        # Right Buttons
        if self._btns[1].fell:
            self._app_idx = (self._app_idx + 1) % len(self._apps)
            self._apps[self._app_idx].switch()

        event = self._keys.events.get()
        if not event or event.key_number >= len(self._apps[self._app_idx].macros):
            return

        app = self._apps[self._app_idx]

        key_number = event.key_number
        pressed = event.pressed

        sequence = app.macros[key_number][2]
        if pressed:
            # 'sequence' is an arbitrary-length list, each item is one of:
            # Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
            # Negative integer: (absolute value) key released
            # Float (e.g. 0.25): delay in seconds
            # String (e.g. "Foo"): corresponding keys pressed & released
            # List []: one or more Consumer Control codes (can also do float delay)
            # Dict {}: mouse buttons/motion (might extend in future)

            if key_number < 12: # No pixel for encoder button
                self.set_pixel(key_number, 0xFFFFFF)

            for item in sequence:
                if isinstance(item, int):
                    if item >= 0:
                        self._keyboard.press(item)
                    else:
                        self._keyboard.release(-item)

                elif isinstance(item, float):
                    time.sleep(item)

                elif isinstance(item, str):
                    self._keyboard_layout.write(item)

                elif isinstance(item, list):
                    for code in item:
                        if isinstance(code, int):
                            self._consumer_control.release()
                            self._consumer_control.press(code)

                        if isinstance(code, float):
                            time.sleep(code)

                elif isinstance(item, dict):
                    if 'buttons' in item:
                        if item['buttons'] >= 0:
                            self._mouse.press(item['buttons'])
                        else:
                            self._mouse.release(-item['buttons'])

                    self._mouse.move(item['x'] if 'x' in item else 0,
                                     item['y'] if 'y' in item else 0,
                                     item['wheel'] if 'wheel' in item else 0)

        else:
            # Release any still-pressed keys, consumer codes, mouse buttons
            # Keys and mouse buttons are individually released this way (rather
            # than release_all()) because pad supports multi-key rollover, e.g.
            # could have a meta key or right-mouse held down by one macro and
            # press/release keys/buttons with others. Navigate popups, etc.
            for item in sequence:
                if isinstance(item, int):
                    if item >= 0:
                        self._keyboard.release(item)

                elif isinstance(item, dict):
                    if 'buttons' in item:
                        if item['buttons'] >= 0:
                            self._mouse.release(item['buttons'])

            self._consumer_control.release()

            if key_number < 12: # No pixel for encoder button
                self.set_pixel(key_number, app.macros[key_number][0])
                self._pixels.show()
