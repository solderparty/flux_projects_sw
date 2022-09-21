import board
import busio

_I2C = None

SW_RIGHT = board.GP0
SW_LEFT = board.GP1
SW_CENTER = board.GP2

SDA = board.GP10
SCL = board.GP11

NEOPIXEL = board.GP29


def I2C():
    global _I2C
    
    if not _I2C:
        _I2C = busio.I2C(SCL, SDA)
    
    return _I2C
