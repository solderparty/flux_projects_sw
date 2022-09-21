import neopixel
import rp2040_stamp_macropad_board as board

from macropad import MacroPad


# Force the on-Stamp Neopixel off
stamp_neo = neopixel.NeoPixel(board.STAMP_NEOPIXEL, 1, brightness=0.2)
stamp_neo.fill(0)

macropad = MacroPad('/apps')

if macropad.apps is None:
    while True:
        pass

macropad.apps[macropad.app_index].switch()

while True:
    macropad.update()
