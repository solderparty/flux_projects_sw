from adafruit_hid.keycode import Keycode

app = {
    'name' : 'Browser',
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE

        # 1st row ----------
        ( 0x004000, '< Back', [ Keycode.CONTROL, Keycode.LEFT_ARROW  ]),
        ( 0x004000, 'Fwd >',  [ Keycode.CONTROL, Keycode.RIGHT_ARROW ]),
        ( 0x400000, 'Up',     [ Keycode.SHIFT, ' ']),

        # 2nd row ----------
        ( 0x202000, '< Tab',  [ Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        ( 0x202000, 'Tab >',  [ Keycode.CONTROL, Keycode.TAB]),

        ( 0x400000, 'Down',   ' '),
        # 3rd row ----------
        ( 0x000040, 'Reload',  [ Keycode.CONTROL, 'r' ]),
        ( 0x000040, 'Home',    [ Keycode.CONTROL, 'H' ]),
        ( 0x000040, 'Private', [ Keycode.CONTROL, 'N' ]),

        # 4th row ----------
        (0x000000, 'Ada',   [ Keycode.CONTROL, 't', -Keycode.CONTROL, 'www.adafruit.com\n']),
        (0x800000, 'Digi',  [ Keycode.CONTROL, 't', -Keycode.CONTROL, 'www.digikey.com\n']),
        (0x101010, 'Hacks', [ Keycode.CONTROL, 't', -Keycode.CONTROL, 'www.hackaday.com\n']),

        # Encoder button ---
        (0x000000, '',      [ Keycode.CONTROL, 'w' ])
    ]
}
