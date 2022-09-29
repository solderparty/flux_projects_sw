import board
import busio

_SPI = None
_I2C = None

LED_R = board.GP0
LED_G = board.GP1
LED_B = board.GP2

SCL = board.GP5
SDA = board.GP4

LCD_CLK  = board.GP6
LCD_COPI = board.GP7
LCD_DC   = board.GP11
LCD_RST  = board.GP12
LCD_CS   = board.GP13

SPK_P = board.GP9
SPK_N = board.GP10

BTN_B      = board.GP14
BTN_A      = board.GP15
BTN_RIGHT  = board.GP16
BTN_DOWN   = board.GP17
BTN_LEFT   = board.GP18
BTN_UP     = board.GP19


def SPI():
    global _SPI
    
    if not _SPI:
        _SPI = busio.SPI(LCD_CLK, MOSI=LCD_COPI)
    
    return _SPI


def I2C():
    global _I2C
    
    if not _I2C: 
        _I2C = busio.I2C(SCL, SDA)
    
    return _I2C
